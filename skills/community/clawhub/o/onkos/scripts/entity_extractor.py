#!/usr/bin/env python3
"""
实体提取器 - 从文本中自动提取角色、地点、物品、事件等实体
增强版: jieba 分词词边界 + posseg 词性标注 + 称谓模式 + 置信度评分 + 题材自适应
核心策略: 以 jieba 分词为单位进行模式匹配，避免 CJK 文本边界问题
根据题材类型(fantasy/urban/wuxia/scifi)自动切换关键词集和事件模式
"""

import os
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from collections import Counter


# ==================== 题材配置 ====================

GENRE_PROFILES = {
    "fantasy": {
        "title_suffixes_2": {"子", "老", "公", "侯", "仙", "母", "祖", "宗", "帝", "王"},
        "title_suffixes_3": {"师兄", "师弟", "师姐", "师妹", "师叔", "师伯", "师尊", "师祖",
                             "道长", "真人", "长老", "掌门", "阁主", "城主", "庄主",
                             "前辈", "阁下", "大人", "公子", "小姐", "姑娘"},
        "title_suffixes_4": {"大长老", "少主", "家主", "族长"},
        "location_keywords": ["山", "峰", "谷", "洞", "湖", "河", "海", "城", "镇", "村",
                              "宫", "殿", "阁", "楼", "院", "门", "岛", "林", "漠", "渊",
                              "塔", "寺", "庙", "观", "府", "庄", "坞", "营", "关", "峡",
                              "泽", "潭", "瀑", "池", "桥", "堤", "港", "湾", "原", "荒"],
        "item_keywords": {
            "功法": ["诀", "功法", "术", "经", "典"],
            "丹药": ["丹", "丸", "散", "液", "露"],
            "法器": ["剑", "刀", "枪", "盾", "印", "钟", "镜", "旗", "塔", "鼎"],
        },
        "event_patterns": [
            (r'突破.{0,4}(淬体|练气|筑基|金丹|元婴|化神|返虚|合体|大乘|渡劫)', "突破", "high"),
            (r'(击败|战胜|打败|斩杀|击退)了?.{0,4}([\u4e00-\u9fff]{2,4})', "战斗", "medium"),
            (r'(获得|得到|收取|炼制)了?([\u4e00-\u9fff]{2,6}?)(?:[，。！？、：；\s""「」『』]|$)', "获取", "medium"),
            (r'(拜师|收徒|入门|出师)', "师承", "high"),
        ],
        "non_name_additions": set(),
    },
    "urban": {
        "title_suffixes_2": {"总", "哥", "姐", "老", "少"},
        "title_suffixes_3": {"总裁", "经理", "主管", "总监", "队长", "局长", "处长", "主任",
                             "先生", "女士", "老板", "教授", "医生", "律师", "警官",
                             "队长", "班长", "连长", "营长"},
        "title_suffixes_4": {"董事长", "总经理", "副局长", "副总", "大队长"},
        "location_keywords": ["楼", "大厦", "广场", "路", "街", "巷", "区", "园", "馆",
                              "店", "厅", "场", "站", "院", "校", "所", "局", "部",
                              "公司", "集团", "中心", "基地", "港口", "机场"],
        "item_keywords": {
            "文件": ["文件", "合同", "协议", "档案", "报告", "方案"],
            "装备": ["枪", "弹", "刀", "甲", "盾", "通讯器", "定位器"],
        },
        "event_patterns": [
            (r'(升职|晋升|降职|辞职|解雇|开除)', "职场", "high"),
            (r'(收购|并购|投资|融资|上市|破产)', "商业", "high"),
            (r'(表白|求婚|分手|结婚|离婚)', "情感", "medium"),
            (r'(暗杀|绑架|劫持|追杀|复仇)', "冲突", "high"),
        ],
        "non_name_additions": {"公司", "集团", "有限", "股份", "有限公", "股份有", "有限公司", "股份有限公司"},
    },
    "wuxia": {
        "title_suffixes_2": {"侠", "仙", "老", "公", "侯", "爷", "僧", "道"},
        "title_suffixes_3": {"掌门", "长老", "堂主", "舵主", "帮主", "盟主",
                             "大侠", "少侠", "女侠", "前辈", "阁下", "师兄", "师弟",
                             "师姐", "师妹", "师叔", "师伯", "掌柜", "镖头"},
        "title_suffixes_4": {"大长老", "总镖头", "副帮主", "副掌门"},
        "location_keywords": ["山", "峰", "谷", "洞", "湖", "河", "城", "镇", "村",
                              "阁", "楼", "院", "门", "岛", "林", "庙", "寺", "观",
                              "府", "庄", "营", "关", "峡", "桥", "港", "湾", "客栈",
                              "镖局", "茶馆", "酒楼"],
        "item_keywords": {
            "武功": ["掌", "拳", "指", "腿", "剑法", "刀法", "功", "诀", "经"],
            "暗器": ["针", "镖", "钉", "砂"],
            "兵器": ["剑", "刀", "枪", "棍", "鞭", "钩", "斧", "锤"],
        },
        "event_patterns": [
            (r'(修炼|练成|领悟|贯通)了?.{0,4}([\u4e00-\u9fff]{2,6})', "武学", "high"),
            (r'(击败|战胜|打退|击退)了?.{0,4}([\u4e00-\u9fff]{2,4})', "战斗", "medium"),
            (r'(拜师|收徒|入门|出师|传授)', "师承", "high"),
            (r'(结拜|结盟|反目|叛出|脱离)', "关系", "medium"),
        ],
        "non_name_additions": set(),
    },
    "scifi": {
        "title_suffixes_2": {"长", "官", "总", "员"},
        "title_suffixes_3": {"舰长", "队长", "司令", "将军", "博士", "教授", "主管",
                             "指挥官", "执行官", "议员", "代表", "顾问", "督察"},
        "title_suffixes_4": {"总指挥", "大将军", "首席执行官", "最高议会"},
        "location_keywords": ["星", "球", "港", "站", "舰", "舱", "区", "层", "基地",
                              "城", "塔", "港", "环", "带", "域", "门", "井", "场",
                              "实验室", "工厂", "矿区", "空间站", "殖民地"],
        "item_keywords": {
            "装备": ["甲", "盾", "枪", "炮", "刃", "盾", "器", "仪"],
            "能源": ["核", "晶", "石", "电池", "反应堆", "引擎"],
        },
        "event_patterns": [
            (r'(突破|突破)了?.{0,4}(基因|能力|等级|阶段)', "进化", "high"),
            (r'(发现|检测|扫描|探测)到?([\u4e00-\u9fff]{2,6})', "发现", "medium"),
            (r'(入侵|攻击|摧毁|占领|解放)了?([\u4e00-\u9fff]{2,6})', "冲突", "high"),
            (r'(叛变|叛逃|投诚|倒戈)', "背叛", "high"),
        ],
        "non_name_additions": {"有限公司", "公司", "集团", "系统", "程序", "协议"},
    },
}


class EntityExtractor:
    """实体提取器 - 自动识别文本中的命名实体，支持题材自适应"""

    # 常见姓氏
    COMMON_SURNAMES = set(
        "赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜"
        "戚谢邹喻柏水窦章苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐"
        "费廉岑薛雷贺倪汤滕殷罗毕郝安常乐于傅皮齐康伍余卜顾孟平黄"
        "萧尹姚邵汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁"
        "杜阮蓝闵席季贾路危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌"
        "万管卢莫经房干解应宗丁宣邓郁杭洪包诸左石崔龚程"
        "邢裴陆荣翁荀羊惠曲家丁段富景詹龙叶幸司"
        "黎白蒲赖卓池乔容向古易廖居步都耿匡国文寇"
    )

    # 复姓
    COMPOUND_SURNAMES = {"欧阳", "司马", "上官", "诸葛", "令狐", "东方", "西门", "南宫",
                         "慕容", "公孙", "独孤", "宇文", "长孙", "轩辕", "端木", "皇甫"}

    # 非人名过滤词
    NON_NAME_WORDS = {
        "这个", "那个", "什么", "怎么", "已经", "可以", "我们", "他们", "自己",
        "这里", "那里", "因为", "所以", "但是", "虽然", "如果", "而且", "或者",
        "不是", "没有", "之后", "之前", "之中", "之间", "以上", "以下",
        "一下", "一点", "起来", "出来", "过来", "回来", "进去", "出去",
        "站着", "坐着", "躺着", "走到", "跑到", "来到",
        "站在", "坐在", "躺在", "走在", "跑在", "飞在", "停在", "留在", "待在",
        "看着", "望着", "想着", "说着", "听着", "跟着", "带着", "拿着", "放着",
        "山巅", "苍茫", "云海", "天地", "江湖", "天下", "世间", "人间",
        "世界", "此时", "此刻", "当下", "瞬间", "忽然", "突然", "竟然",
        "依然", "果然", "居然", "不过", "只是", "然而",
        "说道", "问道", "答道", "喊道", "叫道", "怒道", "笑道",
        "低声", "沉声", "厉声", "大喝", "冷哼", "叹息",
        "可是", "于是", "终于", "只见", "成功", "一定",
        "中的", "手中", "心中", "眼中", "身中",
        "内门", "外门", "入门", "出门", "大门", "房门", "前门", "后门", "侧门",
        "天道", "正道", "邪道", "魔道",
        "今日", "明日", "昨日", "往日", "来日",
        "一声", "两声", "三声", "几声",
        "大事", "小事", "往事", "世事",
        "明白", "知道", "清楚", "发现", "认为", "表示", "希望", "决定", "感觉",
        "准备", "开始", "成为", "属于", "位于", "接近", "返回", "得到", "出现",
        "弟子", "老子", "庄子", "孟子", "孔子", "君子", "才子", "孝子",
        "游子", "赤子", "骄子", "路过", "过来", "起来", "出来",
        # 常见jieba误切词
        "正是", "不是", "只是", "但是", "还是", "或是", "要是", "便是",
        "白皙", "平庸", "俊朗", "清秀", "艳丽", "丑陋", "消瘦", "肥胖",
        "正是王", "正是李", "正是张", "正是陈",
        "走到", "跑到", "飞到", "回到", "来到", "赶到",
        "不停", "不断", "不止", "不了", "不住",
        "之间", "之前", "之后", "之外", "之内", "之上", "之下",
        "一人", "两人", "多人", "众人", "人人",
        "一切", "所有", "全部", "部分", "大多", "少数",
    }

    # 称谓后缀（默认值，初始化时根据题材覆盖）
    TITLE_SUFFIXES_2 = {"子", "老", "公", "侯", "仙", "母", "祖", "宗", "帝", "王"}
    TITLE_SUFFIXES_3 = {"师兄", "师弟", "师姐", "师妹", "师叔", "师伯", "师尊", "师祖",
                        "道长", "真人", "长老", "掌门", "阁主", "城主", "庄主",
                        "前辈", "阁下", "大人", "公子", "小姐", "姑娘"}
    TITLE_SUFFIXES_4 = {"大长老", "少主", "家主", "族长"}

    # 称谓前缀禁用字（名字不能以这些开头）
    TITLE_PREFIX_STOPS = frozenset(
        "你我他她它们这那一不无可其的了是也又都还在将被把向给与于从到为而对"
    )

    # 地点关键词（默认值，初始化时根据题材覆盖）
    LOCATION_KEYWORDS = [
        "山", "峰", "谷", "洞", "湖", "河", "海", "城", "镇", "村",
        "宫", "殿", "阁", "楼", "院", "门", "岛", "林", "漠", "渊",
        "塔", "寺", "庙", "观", "府", "庄", "坞", "营", "关", "峡",
        "泽", "潭", "瀑", "池", "桥", "堤", "港", "湾", "原", "荒",
        "园", "场", "室", "房", "路", "街", "巷",
    ]

    # 修仙/玄幻特有实体（默认值，初始化时根据题材覆盖）
    FANTASY_KEYWORDS = {
        "功法": ["诀", "功法", "术", "经", "典"],
        "丹药": ["丹", "丸", "散", "液", "露"],
        "法器": ["剑", "刀", "枪", "盾", "印", "钟", "镜", "旗", "塔", "鼎"],
        "境界": ["淬体", "练气", "筑基", "金丹", "元婴", "化神", "返虚", "合体", "大乘", "渡劫"]
    }

    # 前缀虚词（用于物品提取过滤）
    ITEM_PREFIX_STOPS = frozenset(
        "的了在是一这那些几得着过不和与被把让给向从到用以而为但或"
    )

    # 实体名首字禁用（动词/介词/副词/代词等不应出现在实体名开头）
    ENTITY_PREFIX_STOPS = frozenset(
        "的了在是一这那些几得着过不和与被把让给向从到用以而为但或"
        "你我他她它们此其哪每某"
        "去来往飞走跑站坐躺手持祭出寻找发路过已正刚才"
        "能会可须需应将敢肯愿当"
    )

    # 物品名内禁用字（物品名中不应包含动词）
    ITEM_INNER_VERBS = frozenset(
        "练修打斗战杀破击防御守攻逃追赶逃躲闪避闪"
    )

    # 地点后缀集合（用于快速判断实体是否更像地名）
    _location_suffix_set = frozenset(LOCATION_KEYWORDS)

    # 物品后缀集合
    _item_suffix_set = frozenset(
        s for suffixes in FANTASY_KEYWORDS.values() for s in suffixes
        if len(s) == 1
    )

    def _looks_like_location(self, name: str) -> bool:
        """判断名称是否更像地名而非人名"""
        if not name:
            return False
        # 以地名关键词结尾
        if name[-1] in self._location_suffix_set and len(name) >= 2:
            # 但排除以姓氏+地名关键词组成的人名（如"林峰"可能是人名）
            if name[0] in self.COMMON_SURNAMES and len(name) == 2:
                return False
            return True
        return False

    def _looks_like_item(self, name: str) -> bool:
        """判断名称是否更像物品名而非人名"""
        if not name:
            return False
        # 以物品关键词结尾
        if name[-1] in self._item_suffix_set and len(name) >= 2:
            # 但排除以姓氏+物品关键词组成的人名（如"陈剑"可能是人名）
            if name[0] in self.COMMON_SURNAMES and len(name) == 2:
                return False
            return True
        return False

    def __init__(self, project_path: str = None, genre: str = None):
        """
        初始化实体提取器

        Args:
            project_path: 项目路径
            genre: 题材类型（fantasy/urban/wuxia/scifi），不指定则从项目配置读取，默认fantasy
        """
        self.project_path = Path(project_path) if project_path else None
        self.known_entities = self._load_known_entities()

        # 题材自适应：确定题材并加载对应配置
        if genre is None and self.project_path:
            genre = self._detect_genre_from_project()
        self.genre = genre or "fantasy"
        self._apply_genre_profile(self.genre)

    def _detect_genre_from_project(self) -> Optional[str]:
        """从项目配置文件读取题材"""
        config_path = self.project_path / "data" / "project_config.json"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                genre = config.get("genre", "")
                # 映射中文题材到 profile key
                genre_map = {
                    "玄幻": "fantasy", "修仙": "fantasy", "仙侠": "fantasy",
                    "都市": "urban", "都市异能": "urban", "现代": "urban",
                    "武侠": "wuxia", "江湖": "wuxia", "古风": "wuxia",
                    "科幻": "scifi", "末世": "scifi", "未来": "scifi",
                }
                return genre_map.get(genre, genre if genre in GENRE_PROFILES else None)
            except Exception:
                pass
        return None

    def _apply_genre_profile(self, genre: str):
        """根据题材加载对应的关键词配置"""
        profile = GENRE_PROFILES.get(genre, GENRE_PROFILES["fantasy"])

        # 覆盖称谓后缀
        self.TITLE_SUFFIXES_2 = profile["title_suffixes_2"]
        self.TITLE_SUFFIXES_3 = profile["title_suffixes_3"]
        self.TITLE_SUFFIXES_4 = profile["title_suffixes_4"]

        # 覆盖地点关键词
        self.LOCATION_KEYWORDS = profile["location_keywords"]
        self._location_suffix_set = frozenset(self.LOCATION_KEYWORDS)

        # 覆盖物品关键词
        self.FANTASY_KEYWORDS = profile["item_keywords"]
        self._item_suffix_set = frozenset(
            s for suffixes in self.FANTASY_KEYWORDS.values() for s in suffixes
            if len(s) == 1
        )

        # 存储事件模式供 _extract_events 使用
        self._genre_event_patterns = profile["event_patterns"]

        # 添加题材特有的非人名过滤词
        self._genre_non_name_additions = profile.get("non_name_additions", set())

    def _load_known_entities(self) -> Dict[str, List[str]]:
        """加载已知实体（优先从 SQLite 知识图谱，兼容旧 JSON）"""
        entities = {"characters": [], "locations": [], "items": []}
        if not self.project_path:
            return entities

        # 优先使用 SQLite 知识图谱
        db_path = self.project_path / "data" / "novel_memory.db"
        if db_path.exists():
            try:
                from knowledge_graph import KnowledgeGraph
                kg = KnowledgeGraph(str(db_path))
                try:
                    for node in kg.list_nodes(node_type="character"):
                        entities["characters"].append(node["name"])
                    for node in kg.list_nodes(node_type="location"):
                        entities["locations"].append(node["name"])
                    for node in kg.list_nodes(node_type="item"):
                        entities["items"].append(node["name"])
                finally:
                    kg.close()
            except Exception:
                pass

        chars_dir = self.project_path / "data" / "characters"
        if chars_dir.exists():
            for char_file in chars_dir.glob("*.json"):
                try:
                    with open(char_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if data.get("name") and data["name"] not in entities["characters"]:
                            entities["characters"].append(data["name"])
                except Exception:
                    pass
        return entities

    def _jieba_segment(self, text: str) -> List[Tuple[str, str]]:
        """使用 jieba posseg 分词并标注词性，返回 (word, flag) 列表"""
        try:
            import jieba.posseg as pseg
            return [(w, f) for w, f in pseg.cut(text)]
        except ImportError:
            # 降级：简单按标点拆分
            parts = re.split(r'([，。！？、：；""「」『』\s])', text)
            return [(p, "x") for p in parts if p.strip()]

    def _jieba_words(self, text: str) -> List[str]:
        """使用 jieba 分词（不带词性），返回词列表"""
        try:
            import jieba
            return list(jieba.cut(text))
        except ImportError:
            return list(text)

    def extract(self, text: str, extract_types: List[str] = None) -> Dict[str, Any]:
        """
        从文本中提取实体

        Args:
            text: 待提取文本
            extract_types: 提取类型

        Returns:
            提取结果（每个实体含 name, type, confidence 字段）
        """
        if extract_types is None:
            extract_types = ["characters", "locations", "items", "events"]

        # 先提取所有类型，用于交叉验证
        all_chars = self._extract_characters(text) if "characters" in extract_types or "all" in extract_types else []
        all_locs = self._extract_locations(text) if "locations" in extract_types or "all" in extract_types else []
        all_items = self._extract_items(text) if "items" in extract_types or "all" in extract_types else []
        all_events = self._extract_events(text) if "events" in extract_types or "all" in extract_types else []

        # 交叉验证：地名和物品名不应出现在角色列表中
        loc_names = {e["name"] for e in all_locs}
        item_names = {e["name"] for e in all_items}
        char_names = {e["name"] for e in all_chars}
        # 题材特有的非人名过滤词
        genre_filter = getattr(self, '_genre_non_name_additions', set())
        # 使用后缀判断补充过滤
        all_chars = [
            e for e in all_chars
            if e["name"] not in loc_names
            and e["name"] not in item_names
            and e["name"] not in genre_filter
            and not self._looks_like_location(e["name"])
            and not self._looks_like_item(e["name"])
            # 角色名不应是地点/物品名的子串（如"天罡"是"天罡剑"的子串）
            and not any(e["name"] in ln and e["name"] != ln for ln in loc_names | item_names)
        ]
        # 跨类型去重：地点/物品名不应是角色名的子串
        all_locs = [
            e for e in all_locs
            if e["name"] not in item_names
            and not any(e["name"] in cn and e["name"] != cn for cn in char_names)
        ]
        all_items = [
            e for e in all_items
            if not any(e["name"] in cn and e["name"] != cn for cn in char_names)
        ]

        result = {
            "characters": all_chars,
            "locations": all_locs,
            "items": all_items,
            "events": all_events,
            "new_entities": []
        }

        # 识别新实体
        known_names = set(self.known_entities.get("characters", []) +
                         self.known_entities.get("locations", []) +
                         self.known_entities.get("items", []))

        for char in result["characters"]:
            name = char["name"] if isinstance(char, dict) else char
            if name not in known_names:
                result["new_entities"].append({"name": name, "type": "character"})

        for loc in result["locations"]:
            name = loc["name"] if isinstance(loc, dict) else loc
            if name not in known_names:
                result["new_entities"].append({"name": name, "type": "location"})

        for item in result["items"]:
            name = item["name"] if isinstance(item, dict) else item
            if name not in known_names:
                result["new_entities"].append({"name": name, "type": "item"})

        return result

    # ==================== 角色提取 ====================

    def _extract_characters(self, text: str) -> List[Dict[str, Any]]:
        """提取角色名（含置信度）"""
        characters = {}  # name -> confidence

        # 方法1：从已知角色匹配（最高置信度）
        for name in self.known_entities.get("characters", []):
            if name in text:
                characters[name] = "high"

        # 方法2：jieba posseg 词性标注
        segmented = self._jieba_segment(text)
        for word, flag in segmented:
            word = word.strip()
            if (flag == "nr"
                    and 2 <= len(word) <= 4
                    and word not in self.NON_NAME_WORDS
                    and word[0] not in self.TITLE_PREFIX_STOPS):
                if word not in characters:
                    characters[word] = "medium"

        # 方法3：称谓模式匹配（基于分词边界）
        # 先将分词结果拼接回文本，利用分词边界确认名称
        self._extract_by_title_pattern(text, characters)

        # 方法4：对话归属识别
        self._extract_from_dialogue(text, characters)

        # 方法5：基于姓氏的精确匹配（仅补充）
        self._extract_by_surname(text, characters, segmented)

        # 去重：短名是长名子串时移除短名
        self._deduplicate_substrings(characters)

        # 过滤低置信度噪音：无姓氏、无称谓、不在已知实体中的low置信度候选
        known_char_names = set(self.known_entities.get("characters", []))
        filtered = {}
        for name, conf in characters.items():
            if conf == "low":
                # low置信度必须是姓氏开头或已知名前缀才保留
                is_surname_start = name[0] in self.COMMON_SURNAMES
                is_compound_surname = any(name.startswith(cs) for cs in self.COMPOUND_SURNAMES)
                is_known_prefix = any(n.startswith(name[:2]) for n in known_char_names)
                if not (is_surname_start or is_compound_surname or is_known_prefix):
                    continue
            filtered[name] = conf
        characters = filtered

        # 构建结果
        result = [{"name": name, "confidence": conf} for name, conf in characters.items()]
        confidence_order = {"high": 0, "medium": 1, "low": 2}
        result.sort(key=lambda x: confidence_order.get(x["confidence"], 3))
        return result

    def _extract_by_title_pattern(self, text: str, characters: Dict[str, str]):
        """基于称谓后缀匹配人名（使用分词边界验证）"""
        words = self._jieba_words(text)
        word_set = set(words)

        # 检查候选名是否与分词边界一致
        def is_word_boundary_match(name: str) -> bool:
            """检查 name 是否是分词结果的某个词或相邻词的组合"""
            if name in word_set:
                return True
            # 检查是否是2个相邻词的组合
            for i in range(len(words) - 1):
                combined = words[i] + words[i + 1]
                if combined == name:
                    return True
            return False

        # 2字称谓后缀（X子/X老/X仙 等）
        for suffix in self.TITLE_SUFFIXES_2:
            pattern = rf'([\u4e00-\u9fff]{{1,2}}{suffix})'
            matches = re.findall(pattern, text)
            for match in matches:
                if (match not in self.NON_NAME_WORDS
                        and len(match) >= 2
                        and match[0] not in self.TITLE_PREFIX_STOPS
                        and is_word_boundary_match(match)):
                    if match not in characters:
                        characters[match] = "high"

        # 3字称谓后缀（X师兄/X道长 等）
        for suffix in self.TITLE_SUFFIXES_3:
            pattern = rf'([\u4e00-\u9fff]{{1,3}}{suffix})'
            matches = re.findall(pattern, text)
            for match in matches:
                if (match not in self.NON_NAME_WORDS
                        and len(match) >= 3
                        and match[0] not in self.TITLE_PREFIX_STOPS
                        and is_word_boundary_match(match)):
                    if match not in characters:
                        characters[match] = "high"
                    # 提取去掉称谓后的名字
                    name_part = match[:-len(suffix)]
                    if (2 <= len(name_part) <= 3
                            and name_part not in self.NON_NAME_WORDS
                            and name_part[0] not in self.TITLE_PREFIX_STOPS
                            and is_word_boundary_match(name_part)):
                        if name_part not in characters:
                            characters[name_part] = "medium"

        # 4字称谓后缀
        for suffix in self.TITLE_SUFFIXES_4:
            pattern = rf'([\u4e00-\u9fff]{{1,3}}{suffix})'
            matches = re.findall(pattern, text)
            for match in matches:
                if (match not in self.NON_NAME_WORDS
                        and len(match) >= 4
                        and match[0] not in self.TITLE_PREFIX_STOPS
                        and is_word_boundary_match(match)):
                    if match not in characters:
                        characters[match] = "high"

    def _extract_from_dialogue(self, text: str, characters: Dict[str, str]):
        """从对话上下文中提取说话者名"""
        # 介词字符
        prep_chars = "对把被向给与将于从到在为而跟同"

        # 对话归属模式
        dialogue_patterns = [
            # "X说道"等 - X前方不能是介词或动词
            (rf'(?<![{prep_chars}])([\u4e00-\u9fff]{{2,4}})(说道|问道|答道|喊道|叫道|怒道|笑道|冷哼道|叹息道|大喝道)', "high"),
            # "X沉声/低声"等 - X前方不能是介词，且X必须是人名（以姓氏开头或已知名）
            (rf'(?<![{prep_chars}])([\u4e00-\u9fff]{{2,3}})(沉声|低声|冷声|厉声|轻声|柔声)', "medium"),
            # "X对Y说" - 分别提取X和Y
            (r'([\u4e00-\u9fff]{2,4})[的]?对([\u4e00-\u9fff]{2,4})(说|道|问)', "medium"),
        ]

        # 动词后缀（提取的名字不应以这些字结尾）
        verb_suffixes = {"说", "道", "问", "答", "喊", "叫", "想", "看", "听",
                         "走", "跑", "站", "坐", "声", "喝", "哼", "来", "去", "过",
                         "起", "下", "上", "出", "入", "回", "到", "在", "着", "了"}

        # 常见动词词尾（名字不应以这些组合结尾）
        verb_endings = {"过来", "起来", "出来", "过来", "回去", "过去", "下来", "上来",
                        "到了", "站着", "坐着", "走着", "飞去", "走去"}

        for pattern, confidence in dialogue_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                for name in match:
                    if (2 <= len(name) <= 4
                            and name not in self.NON_NAME_WORDS
                            and name[-1] not in verb_suffixes
                            and name not in verb_endings
                            and name not in characters
                            and name[0] not in self.TITLE_PREFIX_STOPS
                            and not any(name.startswith(p) for p in ("对", "把", "被", "向", "给", "与"))):
                        # 验证：名字的首字应该是姓氏、已知名开头、或称谓开头
                        first_char = name[0]
                        is_surname = first_char in self.COMMON_SURNAMES
                        is_compound_surname = any(name.startswith(cs) for cs in self.COMPOUND_SURNAMES)
                        is_known_prefix = any(n.startswith(name[:2]) for n in characters)
                        is_title_name = any(name.endswith(ts) for ts in self.TITLE_SUFFIXES_2 | self.TITLE_SUFFIXES_3)

                        if is_surname or is_compound_surname or is_known_prefix or is_title_name:
                            characters[name] = confidence
                        else:
                            # 低置信度 - 可能是误匹配
                            characters[name] = "low"

    def _extract_by_surname(self, text: str, characters: Dict[str, str],
                            segmented: List[Tuple[str, str]]):
        """基于姓氏的精确匹配"""
        # 复姓匹配（优先长名，避免"欧阳明"截断"欧阳明月"）
        for surname in self.COMPOUND_SURNAMES:
            # 尝试2字名(surname+2) -> 1字名(surname+1)，长名优先
            for given_len in (2, 1):
                pattern = rf'({surname}[\u4e00-\u9fff]{{{given_len}}})'
                matches = re.findall(pattern, text)
                for name in matches:
                    if (name not in self.NON_NAME_WORDS
                            and name not in characters
                            and name not in self._location_suffix_set
                            and not self._looks_like_location(name)
                            and not self._looks_like_item(name)):
                        characters[name] = "medium"

        # 从分词结果中找姓氏开头的词（仅补充未识别的）
        for word, flag in segmented:
            word = word.strip()
            if len(word) < 2 or len(word) > 4:
                continue
            if word in characters or word in self.NON_NAME_WORDS:
                continue
            # 跳过复姓开头的词（已在上面处理）
            if any(word.startswith(cs) for cs in self.COMPOUND_SURNAMES):
                continue
            if (word[0] in self.COMMON_SURNAMES
                    and word[0] not in self.TITLE_PREFIX_STOPS
                    and not self._looks_like_location(word)
                    and not self._looks_like_item(word)):
                characters[word] = "low"

    @staticmethod
    def _deduplicate_substrings(entity_dict: Dict[str, str]):
        """去重：短名是长名子串时移除短名"""
        names = list(entity_dict.keys())
        for name in names:
            if name not in entity_dict:
                continue
            for other in names:
                if name != other and other in entity_dict and name in other and len(other) > len(name):
                    if other.startswith(name) or other.endswith(name):
                        entity_dict.pop(name, None)
                        break

    # ==================== 地点提取 ====================

    def _extract_locations(self, text: str) -> List[Dict[str, Any]]:
        """提取地点（含置信度），基于分词边界验证"""
        locations = {}

        # 方法1：从已知地点匹配
        for name in self.known_entities.get("locations", []):
            if name in text:
                locations[name] = "high"

        # 方法2：基于分词结果的地点关键词匹配
        words = self._jieba_words(text)
        word_set = set(words)

        def validate_and_strip(name: str) -> Optional[str]:
            """验证并清理实体名：去除前缀虚词，检查分词边界"""
            # 去除前缀虚词（如"在玄天峰" → "玄天峰"）
            while name and name[0] in self.ENTITY_PREFIX_STOPS:
                name = name[1:]
            if len(name) < 2 or name in self.NON_NAME_WORDS:
                return None
            # 检查分词边界
            if name in word_set:
                return name
            for i in range(len(words)):
                combined = words[i]
                if combined[0] in self.ENTITY_PREFIX_STOPS:
                    continue
                for j in range(i + 1, min(i + 3, len(words))):
                    combined += words[j]
                    if combined == name:
                        return name
                    if len(combined) > len(name):
                        break
            return None

        for kw in self.LOCATION_KEYWORDS:
            pattern = rf'([\u4e00-\u9fff]{{1,3}}{kw})'
            matches = re.findall(pattern, text)
            for match in matches:
                name = validate_and_strip(match)
                if (name
                        and name not in ("内门", "外门", "出门", "入门", "大门",
                                         "房门", "前门", "后门", "侧门", "正道", "邪道")
                        and name not in locations):
                    locations[name] = "medium"

        # 方法3：到达动词 + 地名模式
        arrival_patterns = [
            (r'(?:来到|抵达|到达|回到|返回|前往|赶往|赶赴|飞往|逃往)了?([\u4e00-\u9fff]{2,6}?)(?:[，。！？、：；\s""「」『』]|$)', "high"),
            (r'(?:离开|逃离|逃出|赶出|飞出)了?([\u4e00-\u9fff]{2,6}?)(?:[，。！？、：；\s""「」『』]|$)', "medium"),
            (r'(?:位于|地处|坐落于)([\u4e00-\u9fff]{2,6}?)(?:[，。！？、：；\s""「」『』]|$)', "high"),
        ]

        for pattern, confidence in arrival_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                has_kw = any(kw in match for kw in self.LOCATION_KEYWORDS)
                if (has_kw or len(match) >= 3) and match not in self.NON_NAME_WORDS:
                    if match not in locations:
                        locations[match] = confidence

        # 方法4：jieba posseg 词性标注（ns = 地名）
        try:
            import jieba.posseg as pseg
            for word, flag in pseg.cut(text):
                word = word.strip()
                if flag == "ns" and len(word) >= 2 and word not in self.NON_NAME_WORDS:
                    if word not in locations:
                        locations[word] = "high"
        except ImportError:
            pass

        # 去重
        self._deduplicate_substrings(locations)

        result = [{"name": name, "confidence": conf} for name, conf in locations.items()]
        confidence_order = {"high": 0, "medium": 1, "low": 2}
        result.sort(key=lambda x: confidence_order.get(x["confidence"], 3))
        return result

    # ==================== 物品提取 ====================

    def _extract_items(self, text: str) -> List[Dict[str, Any]]:
        """提取物品/法宝（含置信度），基于分词边界验证"""
        items = {}

        # 方法1：从已知物品匹配
        for name in self.known_entities.get("items", []):
            if name in text:
                items[name] = "high"

        # 方法2：基于分词边界的玄幻关键词匹配
        words = self._jieba_words(text)
        word_set = set(words)

        def validate_and_strip(name: str) -> Optional[str]:
            """验证并清理实体名：去除前缀虚词，检查分词边界"""
            while name and name[0] in self.ENTITY_PREFIX_STOPS:
                name = name[1:]
            if len(name) < 2 or name in self.NON_NAME_WORDS:
                return None
            # 物品名中不应包含动词
            if any(c in self.ITEM_INNER_VERBS for c in name[:-1]):
                return None
            if name in word_set:
                return name
            for i in range(len(words)):
                combined = words[i]
                if combined[0] in self.ENTITY_PREFIX_STOPS:
                    continue
                for j in range(i + 1, min(i + 3, len(words))):
                    combined += words[j]
                    if combined == name:
                        return name
                    if len(combined) > len(name):
                        break
            return None

        for category, suffixes in self.FANTASY_KEYWORDS.items():
            if category == "境界":
                continue
            for suffix in suffixes:
                pattern = rf'([\u4e00-\u9fff]{{1,3}}{suffix})'
                matches = re.findall(pattern, text)
                for match in matches:
                    name = validate_and_strip(match)
                    if name and name not in items:
                        items[name] = "medium"

        # 方法3：动作动词 + 物品模式
        item_action_patterns = [
            (r'(?:取出|拿出|祭出|亮出|掏出|拔出|抽出)了?([\u4e00-\u9fff]{2,4}?)(?:[，。！？、：；\s""「」『』]|$)', "high"),
            (r'(?:手持|手握|身背|腰悬|怀揣)了?([\u4e00-\u9fff]{2,4}?)(?:[，。！？、：；\s""「」『』]|$)', "medium"),
        ]

        for pattern, confidence in item_action_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                has_suffix = any(match.endswith(s) for suffixes in self.FANTASY_KEYWORDS.values()
                                for s in suffixes)
                if (has_suffix or len(match) >= 3) and match not in self.NON_NAME_WORDS:
                    if match not in items:
                        items[match] = confidence

        result = [{"name": name, "confidence": conf} for name, conf in items.items()]
        confidence_order = {"high": 0, "medium": 1, "low": 2}
        result.sort(key=lambda x: confidence_order.get(x["confidence"], 3))
        return result

    # ==================== 事件提取 ====================

    def _extract_events(self, text: str) -> List[Dict[str, Any]]:
        """提取关键事件（根据题材自适应）"""
        events = []

        # 使用题材配置的事件模式
        event_patterns = getattr(self, '_genre_event_patterns', [
            (r'突破.{0,4}(淬体|练气|筑基|金丹|元婴|化神|返虚|合体|大乘|渡劫)', "突破", "high"),
            (r'(击败|战胜|打败|斩杀|击退)了?.{0,4}([\u4e00-\u9fff]{2,4})', "战斗", "medium"),
            (r'(获得|得到|收取|炼制)了?([\u4e00-\u9fff]{2,6}?)(?:[，。！？、：；\s""「」『』]|$)', "获取", "medium"),
            (r'(拜师|收徒|入门|出师)', "师承", "high"),
        ])

        for pattern, event_type, confidence in event_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    desc = "".join(m for m in match if m)
                else:
                    desc = match
                events.append({
                    "type": event_type,
                    "desc": desc,
                    "confidence": confidence
                })

        return events


    def close(self):
        """无资源需释放，保留接口一致性"""
        pass

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action in ("extract", "extract-file"):
            text = params.get("text", "")
            text_file = params.get("text_file")
            if text_file:
                with open(text_file, 'r', encoding='utf-8') as f:
                    text = f.read()
            if not text:
                return {"error": "需要提供文本"}
            types_str = params.get("types", "characters,locations,items,events")
            extract_types = types_str.split(",") if isinstance(types_str, str) else types_str
            return self.extract(text, extract_types)
        else:
            raise ValueError(f"未知操作: {action}")

def main():
    parser = argparse.ArgumentParser(description='实体提取器')
    parser.add_argument('--project-path', help='项目路径')
    parser.add_argument('--action', required=True,
                       choices=['extract', 'extract-file'],
                       help='操作类型')
    parser.add_argument('--text', help='待提取文本')
    parser.add_argument('--text-file', help='待提取文本文件')
    parser.add_argument('--chapter', type=int, help='章节编号（用于实体关联）')
    parser.add_argument('--types', default='characters,locations,items,events',
                       help='提取类型（逗号分隔）')
    parser.add_argument('--genre', choices=['fantasy', 'urban', 'wuxia', 'scifi'],
                       help='题材类型（不指定则从项目配置读取，默认fantasy）')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    extractor = EntityExtractor(args.project_path, genre=args.genre)

    skip_keys = {"project_path", "action", "output", "genre"}
    params = {k: v for k, v in vars(args).items()
              if v is not None and k not in skip_keys and not k.startswith('_')}
    result = extractor.execute_action(args.action, params)
    if args.output == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        for entity_type in ["characters", "locations", "items", "events"]:
            entities = result.get(entity_type, [])
            if entities:
                print(f"\n=== {entity_type} ===")
                for entity in entities:
                    if isinstance(entity, dict):
                        conf = entity.get("confidence", "")
                        name = entity.get("name", entity.get("desc", ""))
                        extra = f" [{conf}]" if conf else ""
                        print(f"  - {name}{extra}")
                    else:
                        print(f"  - {entity}")


if __name__ == '__main__':
    main()
