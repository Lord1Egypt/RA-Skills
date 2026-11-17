# -*- coding: utf-8 -*-
"""
阶段 2.5:新闻摘要生成模块
功能:从数据库查询待输出新闻,用原文关键段落生成摘要(不使用 LLM 改写),存入 digest_output 表
"""
import sys, os
import json
import time
import re
import sqlite3
import urllib.request
from datetime import datetime, timedelta

# 设置 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

# Support standalone execution
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .config import DB_PATH, LLM_MAX_LENGTH, LLM_BATCH_SIZE
except ImportError:
    from config import DB_PATH, LLM_MAX_LENGTH, LLM_BATCH_SIZE

# LLM Configuration (use environment variables, fallback to OpenClaw config)
API_KEY = os.environ.get('NEWS_DIGEST_LLM_API_KEY', '')
BASE_URL = os.environ.get('NEWS_DIGEST_LLM_BASE_URL', '')
MODEL = os.environ.get('NEWS_DIGEST_LLM_MODEL', 'qwen3.6-plus')

def load_llm_config():
    """Fallback: try to load from OpenClaw config if env vars not set"""
    global API_KEY, BASE_URL
    if API_KEY and BASE_URL:
        return True
    # ⚠️ 不在发布的 skill 中读取用户本地配置文件
    # 用户应通过环境变量 NEWS_DIGEST_LLM_API_KEY 和 NEWS_DIGEST_LLM_BASE_URL 配置
    print(f"  ⚠️ LLM not configured. Set NEWS_DIGEST_LLM_API_KEY and NEWS_DIGEST_LLM_BASE_URL.")
    return False

def call_llm(prompt, max_tokens=4000, temperature=0.3):
    """Call LLM API"""
    if not API_KEY or not BASE_URL:
        load_llm_config()
    if not API_KEY or not BASE_URL:
        print(f"  ⚠️ LLM not configured, skipping summary")
        return None
    if not API_KEY:
        return None

    req_data = json.dumps({
        'model': MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': temperature,
        'max_tokens': max_tokens
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/chat/completions',
        data=req_data,
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result.get('choices', [{}])[0].get('message', {}).get('content', '')
    except Exception as e:
        print(f"  ⚠️ LLM API Error: {e}")
        return None

def parse_llm_response(content, news_count):
    """Parse LLM response (仅用于标题修复/改写)"""
    summaries = {}
    pattern = r'\[(\d+)\]\s*(.+?)\n(.+?)(?=\n\n|\[\d+\]|$)'
    matches = re.findall(pattern, content, re.DOTALL)

    for match in matches:
        idx = int(match[0])
        title = match[1].strip()
        summary = match[2].strip()
        summaries[idx] = {'title': title, 'summary': summary}

    return summaries


def is_rhetoric_opening(p):
    """检测是否为宣传语/排比句开头(人民网等站点常见的文学修辞开篇)

    特征:
    - 多条排比: '一条XX...;一条XX...;一条XX...'
    - 文学修辞: '穿山跨海'、'奔流不息' 等四字词语连用
    - 段落开头是宣传语,后面才出现主体
    """
    if not p or len(p) < 30:
        return False

    # 四字成语/修辞词连用: 穿山跨海、奔流不息、沿江驰骋 等
    rhetoric_patterns = [
        '穿山跨海', '奔流不息', '沿江驰骋', '黄金走廊',
        '万里长卷', '东西互济', '南北协同', '陆海统筹',
        '同频共振', '点绿成金', '通江达海', '奋楫扬帆',
        '千帆竞发', '百舸争流', '波澜壮阔', '锦绣大地',
        '蕴含无限', '无限希望', '广袤大地', '春潮涌动',
        '欣欣向荣', '生机勃勃', '风生水起', '日新月异',
        '扬帆起航', '破浪前行', '乘风破浪', '高歌猛进',
    ]
    rhetoric_count = sum(1 for pat in rhetoric_patterns if pat in p)
    if rhetoric_count >= 3:
        return True
    # 单句修辞: 短段落(<50字)含修辞词且无数据/实质动词 → 跳过
    if len(p) < 50 and rhetoric_count >= 1:
        has_substance = bool(re.search(r'(\d+|增长|下降|发布|出台|通过|签署|获批|完成|启动|举行|投产|交付)', p))
        if not has_substance:
            return True

    # 排比特征: 分号分隔 + 重复模式
    semicolons = p.count(';') + p.count(';')
    if semicolons >= 2 and rhetoric_count >= 1:
        return True

    return False


def is_data_card_article(title, content):
    """检测是否为数据卡片型文章(经济日报"权威数读"等)

    特征:
    - 标题含"数读""靓数""数据速览"等关键词
    - 正文包含多个数据点(同比增长、占比等),用分号或句号分隔
    - 文字量短但数据密度高
    """
    if not title:
        return False
    data_card_patterns = [
        '数读', '靓数', '数据速览', '一图看懂', '数据看',
        '权威数读', '数说', '数据盘点', '关键数据',
    ]
    if not any(pat in title for pat in data_card_patterns):
        return False

    # 正文至少包含2个数据点(含数字+单位/百分比)
    data_pattern = re.findall(r'(同比|环比|增长|下降|达到|突破|超|占比|达)[^\d]*\d+[\d,,.%.万亿%千百]*', content or '')
    return len(data_pattern) >= 2


def extract_data_card_summary(title, content, max_chars=LLM_MAX_LENGTH):
    """结构化提取数据卡片型文章的摘要

    策略:
    1. 提取标题中的核心主题
    2. 提取所有数据点(数字+描述)
    3. 去除编辑信息(文案、制作、编辑、记者等)
    4. 生成结构化摘要:每个数据点独立一行
    """
    if not content:
        return title

    text = content.strip()

    # 去除编辑信息(文案、制作、编辑、记者署名等)
    text = re.sub(r'\s*文案[::].*$', '', text)
    text = re.sub(r'\s*制作[::].*$', '', text)
    text = re.sub(r'\s*编辑[::].*$', '', text)
    text = re.sub(r'\s*记者[::].*$', '', text)
    text = re.sub(r'\s*设计[::].*$', '', text)
    text = re.sub(r'\s*策划[::].*$', '', text)
    text = re.sub(r'\s*图表[::].*$', '', text)
    text = re.sub(r'\s*制图[::].*$', '', text)
    # "本文数据来源:XXX"
    text = re.sub(r'\s*本文数据来源[::].*$', '', text)
    # "XX微信公众号"结尾
    text = re.sub(r'\s*.*微信公众号$', '', text)

    text = text.strip()

    # 如果清理后很短,直接返回
    if len(text) < 20:
        return text if text else title

    # 检测数据点分隔方式:分号、句号、叹号、省略号或换行
    # 优先用分号/句号拆分;也支持叹号和省略号(数据卡片常见)
    segments = re.split(r'[;;。!...]+', text)
    segments = [s.strip() for s in segments if s.strip() and len(s.strip()) > 10]

    # 过滤掉引导性话语("本周这些数据最值得关注"等)和编辑信息
    guide_patterns = [
        '最值得关注', '一起来看看', '这些数据', '本周',
        '以下数据', '快来看看', '速览', '一文看懂',
    ]
    editor_patterns = [
        '文案', '制作', '编辑', '记者', '设计', '策划',
        '图表', '制图', '数据来源', '微信公众号',
    ]

    # 提取真正的数据点(含数字+增长/占比等关键词)
    data_points = []
    other_parts = []

    for seg in segments:
        has_data = bool(re.search(r'\d+[\d,,.%.万亿%千百]*', seg))
        is_guide = any(pat in seg for pat in guide_patterns)
        is_editor = any(pat in seg for pat in editor_patterns)

        if has_data and not is_guide and not is_editor:
            data_points.append(seg)
        elif not is_guide and not is_editor:
            other_parts.append(seg)

    # 如果找到了至少2个数据点,生成结构化摘要
    if len(data_points) >= 2:
        lines = []
        # 精简标题:去掉"权威数读|"等前缀
        clean_title = re.sub(r'^(权威数读[||·]|[一图]看懂[||·]|数说[||·])', '', title).strip()
        lines.append(f'**{clean_title}**')

        for dp in data_points:
            # 清理前缀("前5个月"等时间状语保留)
            dp_clean = dp.strip()
            lines.append(f'- {dp_clean}')

        result = '\n'.join(lines)
        if len(result) <= max_chars:
            return result
        return _truncate_at_sentence(result, max_chars)

    # 数据点不足,返回清理后的原文
    return text if text else title


def is_metadata_paragraph(p, title=None):
    """判断一个段落是否是纯元信息(记者署名、来源标注、编辑信息、分享引导等)"""
    if not p or len(p) < 5:
        return True

    # "原标题:XXX"行(人民网等站点的原标题行,通常只含标题不含正文)
    if re.match(r'^原标题[\uff1a:]', p) and len(p) < 150:
        return True

    # 标题行(如果第一段和标题完全相同,跳过)
    if title and p == title:
        return True
    # "机构名:标题"行(如"国家外汇管理局:3月末我国对外金融资产...")
    if title and p.endswith(title):
        return True
    # 标题变体:段落包含标题且不含句号(纯标题行变体)
    if title and len(p) < 200 and title in p and not re.search(r'[。!?]', p):
        return True
    # "题:XXX"行(新华社/人民日报等站点文章正文中的标题行)
    if re.match(r'^题[::]', p) and len(p) < 300:
        return True

    # 作者行:只有作者名(2-3个汉字)或只有短日期
    # 修复(2026-06-24): 上限改为3,避免把"优化产业布局"等4字+内容误判为人名
    if re.match(r'^[\u4e00-\u9fa5]{2,3}\s*$', p):  # 纯中文名(2-3字)
        return True
    if re.match(r'^\d{4}年\d{2}月\d{2}日\s*\d{2}:\d{2}$', p):  # 纯日期(中文格式)
        return True
    # 修复(2026-07-10): ISO 格式日期(中国发展网转载拆行用此格式)
    if re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}$', p):  # 带秒
        return True
    if re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}$', p):  # 不带秒
        return True
    if re.match(r'^\d{4}-\d{2}-\d{2}$', p):  # 仅日期
        return True
    # 修复(2026-07-10): 不带时间的日期也认为是元信息(中国发展网转载拆行)
    if re.match(r'^\d{4}-\d{2}-\d{2}$', p):
        return True
    if re.match(r'^·\s*$', p):  # 纯分隔符
        return True

    # 记者署名行
    if re.match(r'^.*记者[,,::]?\s*[^。]{0,30}$', p) and not re.search(r'[。!?]', p):
        return True
    # 编辑/责编/图文编辑(必须是尾巴,长度<100)
    if re.search(r'(责编|编辑|图文编辑|编辑/设计)', p) and len(p) < 100:
        return True
    # 来源标注(含"数据来源"/"图片来源"/"资料来源"等变体)
    if re.match(r'^(?:数据|图片|资料)?来源[\uff1a:]', p) and len(p) < 100:
        return True
    # 制图署名(人民网图表新闻常见: "制图：蔡华伟")
    if re.match(r'^制图[\uff1a:]', p) and len(p) < 50:
        return True
    # 公众号/分享引导
    if re.search(r'(关注.*公众|分享让.*人|分享让.*看)', p) and len(p) < 100:
        return True
    # XX微信公众号/XX公众号(来源标注,夹在来源:和分享之间)
    if re.search(r'微信公众号$', p) and len(p) < 50:
        return True
    # 微信扫码(中宏网等站点的分享按钮文本)
    if re.match(r'^用微信扫描二维码', p):
        return True
    # 修复(2026-07-10): 来源名单独成行(中国发展网转载拆行)
    # 经济参考报、新华网、科技日报等来源名
    if re.match(r'^[\u4e00-\u9fa5]{2,10}(报|日报|周报|网|社|台|新闻网)$', p) and len(p) < 20:
        return True
    # 站点名+网讯(单独成行时)
    if re.match(r'^[\u4e00-\u9fa5]+网讯$', p) and len(p) < 20:
        return True
    # 修复(2026-07-08): 尾部电头署名(如"本报雄安电" "经济日报雄安电")单独成行
    if re.match(r'^(?:本报|[\u4e00-\u9fa5]+报)[\u4e00-\u9fa5]{1,8}电\s*$', p) and len(p) < 30:
        return True
    # 修复(2026-07-10): "摘要：" 单独成行(中国发展网转载时拆成多行)
    if p.strip() == '摘要：' or p.strip() == '摘要:':
        return True
    # 时间戳行
    if re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', p) and len(p) < 50:
        return True
    # 修复(2026-07-10): 中国发展网等转载新华网文章的 '日期 时间 来源摘要：' 格式
    # 例: '2026-07-10 11:06新华网摘要：'
    if re.match(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s*\w+摘要[：:]', p) and len(p) < 60:
        return True
    # 版权/转载
    if re.search(r'(本文由.*原创|转载.*说明|违规转载|本文图片来自)', p) and len(p) < 150:
        return True
    # 括号括起来的信息(通常是非正文)
    if re.match(r'^[((].*[))]$', p) and len(p) < 60:
        return True
    # 纯图片说明/空行
    if re.match(r'^[\s\u3000]*$', p):
        return True
    # 图片说明: "图为XX..."
    if re.match(r'^图为', p) and len(p) < 100:
        return True
    # 摄影署名: "初宝瑞摄(影像中国)"
    if re.match(r'^.+摄[\uff08(]', p) and len(p) < 80:
        return True
    # 报纸版次: "《 人民日报 》( 2026年06月11日   10 版)"(支持全角/半角括号)
    if re.search(r'《.+》.*[\uff08(].*\d{4}年.*\d+.*版[\uff09)]', p) and len(p) < 150:
        return True
    # 图片说明: "YYYY年M月D日,在XX,一名XX做XX。新华社XXX摄"
    # 特征: 以日期开头,含地点+人物+动作,末尾有"XX摄"或"新华社记者XXX摄"
    if re.match(r'^\d{4}年\d{1,2}月\d{1,2}日.*?(摄$|[。]\s*[^。]+摄[。]?)', p) and len(p) < 200:
        return True

    return False


def clean_paragraph_text(p):
    """清理段落内的元信息标签(记者名、电头等)"""
    text = p

    # 去除开头的电头(支持含数字的日期)
    # 修复(2026-06-24): 同时处理"本报讯(记者XXX)"格式,避免留下空括号
    # 修复(2026-06-29): 允许"讯"和括号之间有空格(如"科技日报讯 (关悦 记者陈瑜)")
    text = re.sub(r'^[\u4e00-\u9fa5]{2,4}讯[\s]*[\uff08(][^\uff09)]*[\uff09)][\s]*', '', text)
    text = re.sub(r'^本报讯[\s]*[\uff08(][^\uff09)]*[\uff09)][\s]*', '', text)
    text = re.sub(r'^[\u4e00-\u9fa5]+网[\u4e00-\u9fa5]*讯[\s]*[\uff08(][^\uff09)]*[\uff09)][\s]*', '', text)
    text = re.sub(r'^新华社\S+?电[\s]*[\uff08(][^\uff09)]*[\uff09)][\s]*', '', text)
    # 修复(2026-07-10): 中国发展网等转载的 "日期 时间 来源摘要：" 前缀
    text = re.sub(r'^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}\s*\w+摘要[\uff1a:]\s*', '', text)
    # 也处理无括号的情况(如"本报讯 "、"新华社XX电")
    text = re.sub(r'^[\u4e00-\u9fa5]{2,4}讯\s*', '', text)
    text = re.sub(r'^本报讯\s*', '', text)
    text = re.sub(r'^[\u4e00-\u9fa5]+网[\u4e00-\u9fa5]*讯\s*', '', text)
    text = re.sub(r'^新华社\S+?电\s*', '', text)
    # XX网XX消息(记者XXX)/(总台记者XXX)(央广网/人民网/新华社等)
    # 修复(2026-07-05 上午): 括号内允许"总台记者"、"XX台记者"等前缀(如"央广网北京7月5日消息（总台记者胡晓辉 河南台记者刘佳 卢怀涛）")
    # 修复(2026-07-05 中午): 同时兼容半角括号 ( 和全角括号 （
    text = re.sub(r'^[\u4e00-\u9fa5]+[网社台][\u4e00-\u9fa5\d]+消息[\uff08(][^\uff09)]*?记者[^\uff09)]*[\uff09)]\s*', '', text)
    # 广播/通讯社报道前缀("据中央广播电视总台...报道" "据新华社报道")
    # 修复(2026-06-18): [,,::、]? 吃掉报道后的标点,避免留下 ",国务院..." 类残前缀
    # 修复(2026-07-05 上午): 补全角逗号 [,,，::、]，央广网等站点用全角逗号
    # 修复(2026-07-16): 限制只匹配含网/社/台/新闻标识的真正媒体前缀,
    #   避免误杀"据《科学》杂志报道"等学术引用
    text = re.sub(r'^据[^,，。]{0,30}?[网社台](?:[^,，。]*?记者)?[^,，。]*?报道[,,，::、]?\s*', '', text)
    text = re.sub(r'^据[^,，。]{0,20}?新闻[^,，。]*?报道[,,，::、]?\s*', '', text)
    text = re.sub(r'^据新华社报道[,,，::、]?\s*', '', text)
    text = re.sub(r'^据本报记者.*?报道[,,，::、]?\s*', '', text)
    # 本报/XX报/XX网/XX社 XX电 (支持含数字的日期)
    # 注意:不用[网社台]宽匹配,避免匹配到"中央广播电视总台"等正文中的"台"
    # 修复(2026-07-12): 限制报/网/社最多12字,且"电"后必须是空格/换行/括号/结尾,避免误匹配"电子/电动/电池"等词
    text = re.sub(r'^(?:本报|[\u4e00-\u9fa5]{1,4}报|[\u4e00-\u9fa5]{2,5}网|[\u4e00-\u9fa5]{2,5}社)[\u4e00-\u9fa5\d月日\s]{2,12}电(?=\s|[\uff08()]|$)\s*', '', text)

    # === 科创版日报/财联社电头格式 ===
    # 《XX日报》X月X日讯(编辑 XXX)/ 财联社X月X日讯(编辑 XXX)
    # 特征:开头是媒体名(可能带书名号)+ 日期 + 讯 +(编辑 XXX)
    text = re.sub(r'^[\uff08《]*[\u4e00-\u9fa5]{2,15}[》)]?\d{1,2}月\d{1,2}日讯[\uff08(]编辑[^\uff09)]*[\uff09)]\s*', '', text)

    # === 新增:覆盖科创版日报/财联社电头格式 ===
    # 《XX日报》X月X日讯(编辑 XXX)/ 财联社X月X日讯(编辑 XXX)
    # 特征:开头是媒体名+日期+讯+编辑信息,可能带书名号
    if re.match(r'^[\uff08《]*[^》》]*[》)]?\s*[\u4e00-\u9fa5]{2,10}\d{1,2}月\d{1,2}日讯[\uff08(]编辑', text):
        # 整行是电头,清空
        if len(text) < 100:  # 电头行通常较短
            return text.strip()
        # 如果很长(电头后跟正文),只删除电头部分
        text = re.sub(r'^[\uff08《]*[^》》]*[》)]?\s*[\u4e00-\u9fa5]{2,10}\d{1,2}月\d{1,2}日讯[\uff08(]编辑[^\uff09)]*[\uff09)]\s*', '', text)

    # 去除 "XX报记者XXX从XX获悉" / "记者XXX从XX获悉" (可能在日期之后)
    # 注意: 记者名字用负向前瞻排除"从",避免名字正则吃掉"从XX获悉"整段
    # 修复(2026-06-18): {0,4}→{1,4},只删除有记者署名的情况("记者XXX从...获悉");
    #   "记者从...获悉"是新闻正文(如"记者从发布会获悉,XXX将于..."),不应删除
    # 修复(2026-06-21): "获悉"后紧跟具体事实的,不应删除整个获悉结构
    if re.search(r'从[^,,。]+获悉[^,,。]*近日[^,,。]*(联合印发|联合发布|印发|出台|发布|联合制定)', text):
        # 保留正文,只删记者署名前缀(如"工人日报北京6月10日电(记者杨召奎)")
        # 修复(2026-06-24): 负向前瞻排除非记者名(今天/近日/从/发现等),避免误删"记者今天了解到"
        text = re.sub(r'^[\u4e00-\u9fa5]*报?记者(?:(?!从|今天|近日|日前|了解到|获悉|发现|看到|走访|调研|前往|深入)[\u4e00-\u9fa5]){2,6}[,,::、、]?\s*', '', text)
    # 修复(2026-06-24): "记者今天了解到" 等正文开头,不能被当记者署名删除
    elif re.match(r'^记者(?:(?!今天|近日|日前|了解到|获悉|从|发现|看到|走访|调研|前往|深入|表示)[\u4e00-\u9fa5]){2,4}[,,]', text):
        text = re.sub(r'^记者(?:[\u4e00-\u9fa5]{2,4}[,,])\s*', '', text)
    # 修复(2026-06-24): "记者XXX了解到/获悉/表示" 等常见正文开头,不应被当记者署名删除
    # 只删除真正的记者署名(2+字人名+逗号/冒号等分隔符+报道/从)
    elif re.match(r'^记者\s+(?!今天|近日|日前|了解到|获悉|从|发现|看到|走访|调研|前往|深入)[\u4e00-\u9fa5]{2,6}', text):
        text = re.sub(r'^记者\s+[\u4e00-\u9fa5]{2,6}[,,::、]?\s*', '', text)
    else:
        # 修复(2026-06-21): "获悉"后跟具体事实/数据/事件的,保留获悉结构后的实质内容
        # 只删除纯粹的获悉套话(后面没有实质内容)
        huoxi_match = re.search(r'(?:从[^,,。]+)?获悉[,,::、]?\s*', text)
        if huoxi_match:
            after = text[huoxi_match.end():].strip()
            # 如果获悉后紧跟实质内容(数据/事件/研究结果),保留获悉后的内容但删除获悉前缀
            if len(after) > 50 or re.search(r'(发布|印发|出台|发表|通过|发现|签署|增长|突破|达到)', after):
                # 删除记者署名前缀 + 获悉前缀,保留后文
                text = re.sub(r'^[\u4e00-\u9fa5]*报?记者(?:(?!从|今天|近日|日前|了解到|获悉|发现|看到|走访|调研|前往|深入)[\u4e00-\u9fa5]){2,6}[,,::、、]?\s*(?:从[^,,。]+)?获悉[,,::、、]?\s*', '', text)
            else:
                # 修复(2026-06-21): "获悉"后跟具体事实/数据/事件的,保留获悉结构后的实质内容
                # 只删除纯粹的获悉套话(后面没有实质内容)
                # 修复(2026-06-24): 加括号匹配[\uff08(]?和[\uff09)]?,避免"(记者黄洪涛)"删后留下空括号
                text = re.sub(r'[\uff08(]?[\u4e00-\u9fa5]*报?记者(?:(?!从|今天|近日|日前|了解到|获悉|发现|看到|走访|调研|前往|深入)[\u4e00-\u9fa5]){2,6}[,,::、、]?\s*(?:从[^,,。]+获悉[,,::、、]?\s*)?[\uff09)]?', '', text)
        else:
            text = re.sub(r'[\uff08(]?[\u4e00-\u9fa5]*报?记者(?:(?!从|今天|近日|日前|了解到|获悉|发现|看到|走访|调研|前往|深入)[\u4e00-\u9fa5]){2,6}[,,::、、]?\s*(?:从[^,,。]+获悉[,,::、、]?\s*)?[\uff09)]?', '', text)
    # "(记者XXX)" 或 "(记者 XXX)" 括号残留
    text = re.sub(r'[((]记者[\u4e00-\u9fa5\s\xa0]+[))]', '', text)
    # 空括号残留: "()"或"( )"
    text = re.sub(r'[((]\s*[))]', '', text)
    # "本报记者XXX报道/表示" 等
    text = re.sub(r'本报记者.*?(?:报道|表示|说|称)[::]?\s*', '', text)
    # "(记者XXX)" 或 "(记者 XXX)" 括号残留
    text = re.sub(r'[((]记者[\u4e00-\u9fa5\s\xa0]+[))]', '', text)
    # 空括号残留: "()"或"( )"
    text = re.sub(r'[((]\s*[))]', '', text)
    # "本报记者XXX报道/表示" 等
    text = re.sub(r'本报记者.*?(?:报道|表示|说|称)[::]?\s*', '', text)
    # "原标题:XXX" 去除原标题前缀(支持半角/全角冒号)
    text = re.sub(r'^原标题[\uff1a:]\s*', '', text)
    # 出席名单长句(含多个职务+人名) - 截断到出席名单前
    text = re.sub(r'[,,]\s*中国银联董事长.*$', '', text)
    # "(刘文文)" 记者署名前缀
    text = re.sub(r'^\([\u4e00-\u9fa5]+\)', '', text)
    # "(王云杉、薛子怡)" 记者署名前缀(全角括号+多人名)
    text = re.sub(r'^[\uff08(][\u4e00-\u9fa5\u3001、,,\s]+[\uff09)]', '', text)

    # 去除末尾的记者署名行 "(科技日报 XXX XXX)" / "(科技日报 XXX XXX)"
    # 修复:[\s\u3000\xa0] 覆盖全角空格、不换行空格等,避免署名中的空格漏匹配
    text = re.sub(r'\s*[\uff08(]?(?:科技日报|本报记者|记者)[\u4e00-\u9fa5\s\u3000\xa0]{2,30}[\uff09)]?\s*$', '', text)
    # 修复(2026-07-08): 尾部电头署名 "本报XX电" (如"本报雄安电" "经济日报雄安电")
    # 特征: 以"报"字后接地点+"电"结尾,或整段就是这种模式
    text = re.sub(r'\s*(?:本报|[\u4e00-\u9fa5]+报)[\u4e00-\u9fa5]{1,8}电\s*$', '', text)
    # 去除 "来源:XXX" 尾巴
    text = re.sub(r'\s*来源[::].*$', '', text)
    # 修复(2026-06-30): 拼接后"本报讯(记者XXX)"出现在段落中间,需清理
    # 例: "(责任编辑:XXX)本报讯 （记者XXX）正文..."
    text = re.sub(r'[\uff08(]?[\u4e00-\u9fa5]*报?本报讯[\s]*[\uff08(][^\uff09)]*[\uff09)]\s*', '', text)
    text = re.sub(r'[\uff08(]?[\u4e00-\u9fa5]*报?本报讯\s*(?=[\u4e00-\u9fa5]{2,6}[\uff08(])', '', text)
    # 修复(2026-07-01): 清理段落中间的记者署名和来源标注
    # 例: "...561.69亿元。（新甘肃·甘肃日报记者曹立萍）" → "...561.69亿元。"
    # 模式: 句号/括号 + 来源名 + 记者/记者名 + 右括号
    text = re.sub(r'[\uff08(]?[\u4e00-\u9fa5]+[\uff08\uff0e·]+[\u4e00-\u9fa5]*日报[\u4e00-\u9fa5]*记者[\u4e00-\u9fa5\s\u3001、]{1,10}[\uff09)]?\s*$', '', text)
    text = re.sub(r'[\uff08(](?:新[\u4e00-\u9fa5]+)?[\u4e00-\u9fa5]+日报[\u4e00-\u9fa5]*记者[\u4e00-\u9fa5\s\u3001、]{1,10}[\uff09)]', '', text)

    return text.strip()


def extract_original_summary(content, title, max_chars=LLM_MAX_LENGTH):
    """从新闻原文提取关键段落作为摘要(不改写)

    策略升级:
    1. 按段落拆分,跳过纯元信息段落(记者署名、来源标注等)
    2. 清理每段内的电头、记者名
    3. 短新闻(全文<300字)直接返回全文
    4. 首段有干货(长+有动词/数据) → 首段即摘要
    5. 首段太水 → 取后续2-3段拼接
    6. 截断到 max_chars,优先保留完整句子
    """
    if not content or len(content.strip()) < 20:
        return ''

    # 修复(2026-06-28): 人民网等站点 dateline 被 HTML 解析打断(如"人民网北京6月2\n8\n日电")
    # 修复(2026-07-02): 人民网 dateline 被多段拆分("人民网北京7月\n2\n日电\n（记者\n乔雪峰\n）")
    # 通用方案: 将所有极短行(≤3字)合并到上一行
    # 修复(2026-07-10): 保留"摘要："等特殊标记行,不合并到上一行(中国发展网转载拆行)
    special_markers = ['摘要：', '摘要:']
    lines = content.split('\n')
    merged_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and len(stripped) <= 3:
            # 修复(2026-07-10): 摘要：和来源名(新华网等)单独保留
            is_source_short = bool(re.match(r'^[\u4e00-\u9fa5]+[网社台]$', stripped))
            if stripped in special_markers or is_source_short:
                merged_lines.append(stripped)
            elif merged_lines:
                merged_lines[-1] += stripped
        elif stripped:
            merged_lines.append(stripped)
    content = '\n'.join(merged_lines)
    # 修复(2026-07-02): 合并后如果行首以）开头,去掉它(上一行以（结尾,记者署名被拆断)
    # 更通用的方案: 去掉以）或)开头的孤立短段落,并把它合并到前一段落
    cleaned_lines = []
    for line in content.split('\n'):
        if line.startswith(('）', ')')) and cleaned_lines:
            cleaned_lines[-1] += line
        else:
            cleaned_lines.append(line)
    content = '\n'.join(cleaned_lines)

    # 按段落拆分
    # 修复(2026-07-02): 去掉以）或)开头的内容(上一行的（被当作元信息段落跳过了)
    paragraphs = [p.strip() for p in re.split(r'\n+', content) if p.strip()]
    cleaned_paragraphs = []
    for p in paragraphs:
        if p.startswith(('）', ')')) and cleaned_paragraphs:
            # 孤立的）合并到上一段
            cleaned_paragraphs[-1] += p
        else:
            cleaned_paragraphs.append(p)
    paragraphs = cleaned_paragraphs
    # 修复(2026-07-02): 如果段落以）开头,说明(被元信息段落吞掉了,去掉孤立的）
    paragraphs = [re.sub(r'^）', '', p) if p.startswith('）') else p for p in paragraphs]

    if not paragraphs:
        return ''

    # 修复(2026-06-24): 去除末尾重复的段落(视频站点模板把开头导语在末尾又复制一遍)
    if len(paragraphs) > 2:
        first = paragraphs[0]
        for i in range(len(paragraphs) - 1, 0, -1):
            if paragraphs[i] == first:
                paragraphs = paragraphs[:i]
                break
            # 也处理前缀匹配(末尾段落是首段的截断版本)
            if len(paragraphs[i]) > 20 and first.startswith(paragraphs[i]):
                paragraphs = paragraphs[:i]
                break

    # 修复(2026-07-21): 中国发展网转载时插入了"摘要："标签+摘要内容区块
    # 检测到摘要标签后,同时跳过紧随的摘要内容段落
    skip_summary_block = False

    # 跳过开头连续的元信息段落(电头、日期、站点名、分享按钮等)
    # 同时跳过宣传语/排比句开头(人民网等站点的文学修辞开篇)
    start_idx = 0
    skip_empty_count = 0
    for i, p in enumerate(paragraphs):
        if i >= 15:  # 最多跳过15个(覆盖中宏网等多元信息站点)
            break

        # 修复(2026-07-21): 摘要标签 + 紧随摘要内容,一起跳过
        if p.strip() == '摘要：' or p.strip() == '摘要:':
            skip_summary_block = True
            start_idx = i + 1
            continue
        if skip_summary_block:
            # 紧随摘要标签的那段摘要内容,跳过
            skip_summary_block = False
            start_idx = i + 1
            continue

        # 修复(2026-06-17): "一是/二是/三是"等编号段落不是元信息,不应被跳过
        # 只跳过确认的元信息和极短段落(<10字且不含数字/序号)
        is_meta = is_metadata_paragraph(p, title)
        # 极短段落(<10字): 跳过纯符号/空格,但保留编号段(一/二/三/第/1/2/开头)
        if len(p) < 10:
            has_list_marker = bool(re.match(r'^[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u7b2c1234567890]', p))
            if not has_list_marker:
                is_meta = True
        is_rhetoric = is_rhetoric_opening(p)
        if is_meta or is_rhetoric:
            start_idx = i + 1
            if is_rhetoric:
                skip_empty_count += 1
        else:
            break

    # 如果跳过了宣传语段落,打印提示(便于调试)
    if skip_empty_count > 0:
        print(f"  [跳过宣传语开头] {skip_empty_count} 段")

    # 提取并清理正文段落
    clean_parts_raw = []
    for i in range(start_idx, len(paragraphs)):
        p = paragraphs[i]

        # 修复(2026-06-17): 跳过纯元信息段落(记者署名、来源标注等)
        # 但不跳过编号段落(一是/二是等)和实质性短段
        is_meta = is_metadata_paragraph(p, title)
        # 编号段落(一是/二是/三是/1./2.等)不是元信息
        if is_meta and len(p) < 10:
            has_list_marker = bool(re.match(r'^[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u7b2c1234567890]', p))
            if has_list_marker:
                is_meta = False

        if is_meta:
            # 纯元信息: 如果已经收集了正文,就停止;否则继续跳过
            if clean_parts_raw:
                break
            continue

        # 清理段落(电头、记者名等)
        cleaned = clean_paragraph_text(p)
        if not cleaned:
            continue

        clean_parts_raw.append(cleaned)

    # 修复(2026-06-17): 央广网等站点将每条政策各占一行,导致段落被切碎
    # 合并相邻短段(<30字)为逻辑段落,避免首段丢失
    clean_parts = []
    buf = ''
    for part in clean_parts_raw:
        if len(part) < 30:
            # 短段,追加到缓冲区
            buf = (buf + ' ' + part).strip()
        else:
            # 长段,先flush缓冲区
            if buf:
                clean_parts.append(buf)
                buf = ''
            clean_parts.append(part)
    # flush 残余缓冲区
    if buf:
        # 缓冲区追加到最后一个clean_parts(或独立成段)
        if clean_parts:
            clean_parts[-1] = (clean_parts[-1] + ' ' + buf).strip()
        else:
            clean_parts.append(buf)

    if not clean_parts:
        return ''

    # === 新策略:智能分级提取 ===

    # 计算清洗后的全文长度
    full_clean = ' '.join(clean_parts)

    # 0b. 去除标题重复开头(部分站点正文首句与标题完全相同)
    # 如: 标题"多措并举净化投资环境",正文开头"多措并举净化投资环境 近日,..."
    if clean_parts and title:
        first = clean_parts[0]
        # 检测首句是否与标题重复(前缀匹配或完全匹配)
        if first == title or first.startswith(title + ' ') or first.startswith(title + '\u3000'):
            # 去掉标题重复部分,保留剩余内容
            remainder = first[len(title):].lstrip(' \u3000')
            if remainder:
                clean_parts[0] = remainder
            else:
                clean_parts.pop(0)  # 整句都是标题,直接移除
            if clean_parts:
                full_clean = ' '.join(clean_parts)
            else:
                return title  # 只剩标题,无法生成摘要

    # 0. 数据卡片型文章:结构化提取数据点
    # (放在短新闻判断之前,因为数据卡片往往很短但信息密度高)
    if is_data_card_article(title, full_clean):
        return extract_data_card_summary(title, full_clean, max_chars)

    # 修复(2026-06-25): 去除全文重复(短新闻站点把同一段内容复制两次)
    # 检测: 前一半内容在后一半中完整出现 → 只保留一份
    if len(full_clean) > 100:
        half = len(full_clean) // 2
        for chunk_len in range(min(half, 80), 30, -10):
            chunk = full_clean[:chunk_len]
            idx = full_clean.find(chunk, chunk_len)
            if idx > 0:
                # 找到重复点,截断到第一次出现
                full_clean = full_clean[:idx]
                # 重新拆分
                clean_parts = full_clean.split(' ') if ' ' in full_clean else [full_clean]
                print(f"  [去除全文重复] 截断到 {len(full_clean)} 字符")
                break

    # 1. 短新闻:全文<450字,直接返回全文
    # 修复(2026-06-30): 经济日报/央广网短讯在 300-450 字范围,本可完整保留,之前阈值300导致被截断
    if len(full_clean) < 450:
        return _clean_tail_datelines(full_clean)

    # 2. 首段判断:首段>80字且有干货(动词/数据)
    # 注意:排除纯表态词(表示/指出/声称/认为/强调),这些不含实质信息
    first_para_raw = clean_parts[0] if clean_parts else ''
    first_para_raw_len = len(first_para_raw)  # 清理前原始长度(修复新华网电头缩水问题)
    first_para = clean_parts[0] if clean_parts else ''
    # 修复(2026-06-29): 新增"投运/通车/通航/竣工/交付/签约/揭牌/投产"等工程/基础设施类动词
    # 修复(2026-07-16): 新增科研/技术类动词(开发/揭示/提升/解决/实现/构建)
    # 修复(2026-07-24): 新增科研成果动词(造出|发表于|在线发表|获悉|发现|揭示|研制|合成|制备|攻克)
    has_action = bool(re.search(r'(发布|通过|增长|突破|签署|获批|下降|完成|推出|印发|出台|实施|启动|举行|投运|通车|通航|竣工|交付|签约|揭牌|投产|开发|揭示|提升|解决|实现|构建|造出|发表于|在线发表|获悉|发现|揭示|研制|合成|制备|攻克)', first_para))
    # 修复(2026-07-16): 新增"倍/次"(如5000倍提升/3次刷新纪录),匹配科研突破/技术进展
    # 修复(2026-07-24): 新增"日"(科研新闻"X月X日"日期格式)和"第"(第X次/第X代/第X篇)
    has_data = bool(re.search(r'\d+(万|亿|元|%|千|百|倍|次|日|第)', first_para))

    # 去除首段中的残乱前缀(如"息据""消息称据"等抓取异常导致的乱码前缀)
    # 模式: 1-2个汉字+"据",且不在句首合理位置
    first_para_clean = re.sub(r'^[\u4e00-\u9fa5]{1,2}(?=[据报])', '', first_para)
    if first_para_clean != first_para:
        clean_parts[0] = first_para_clean
        first_para = first_para_clean
        full_clean = ' '.join(clean_parts)

    # 检测首段是否以冒号结尾(预告句/导语),必须拼接后续内容
    # 修复(2026-06-17): 央广网等站点首段以冒号结尾,后续才是干货
    ends_with_colon = first_para.endswith((':', ':'))
    # 修复(2026-06-24): 次段以冒号结尾也是预告句,需拼接后续内容(如"从六方面提出具体举措:")
    second_ends_with_colon = len(clean_parts) > 1 and clean_parts[1].endswith((':', ':'))

    # 检测首段是否为叙事型开头(患者故事、场景描写、新闻特写等)
    # 特征:以人物/场景开头,用文学手法描述,不含核心事实
    # 修复(2026-07-24): 排除"X月X日从XX获悉"标准科研新闻导语(不是叙事型)
    is_standard_lead = bool(re.search(r'\d{1,2}月\d{1,2}日从[^。]+获悉', first_para))
    is_narrative = (not is_standard_lead) and bool(re.search(r'(近日|日前|最近)[^。]{0,100}(患者|眉头紧锁|攥着|皱起眉头|坐在.*面前|推开.*门|走进.*大厅|来到.*现场|一位.*患者|一位.*老人)', first_para))
    # 或者:首段主要是场景描写+人物动作,无政策/数据/会议/发布等硬核信息
    no_hard_info = not any(kw in first_para for kw in ['发布', '印发', '出台', '召开', '举行', '签约', '上市', '获批', '通过', '增长', '突破', '亿', '万', '元'])
    has_person_focus = bool(re.search(r'(患者|老人|市民|村民|学生|老师)(.*?)(攥着|皱着|坐在|走进|来到|推开|拿着|握着)', first_para))
    if no_hard_info and has_person_focus:
        is_narrative = True

    # 检测首段是否为表态型开头(发言人表示/指出/声称...但无具体数据)
    # 特征:含表态动词但无具体数据/事实,实质内容在后续段落
    # 修复(2026-06-17): "称"单字会误杀"以下简称/名称/堪称"等,改为"声称/宣称"
    # 修复(2026-06-21): 排除科研场景的"表示"(学者表示研究成果),以及含实质事实的段落
    # 修复(2026-07-24): 排除"从XX获悉"标准新闻导语(即使无数据也非表态型)
    is_statement_only = False
    if not has_data and not is_standard_lead:
        statement_match = re.search(r'(表示|指出|声称|宣称|认为|强调)', first_para)
        if statement_match:
            # 排除科研场景: "研究员/教授/学者/团队/XX表示"
            is_academic = bool(re.search(r'(研究员|教授|学者|团队|院士|博士|主任|院长|专家).*?表示', first_para))
            # 排除含实质事实: 含研究/开发/发布/发现/通过/增长等硬核动词
            # 修复(2026-07-24): 增加造出|合成|制备|攻克|发表于|在线发表|获悉|揭示|研制
            has_substance = bool(re.search(r'(开发|发布|发现|通过|联合|实现|构建|推出|上线|签署|成立|完成|突破|在线发表|造出|合成|制备|攻克|发表于|获悉|揭示|研制)', first_para))
            if not is_academic and not has_substance:
                is_statement_only = True

    if is_statement_only and len(clean_parts) > 1:
        # 表态型:跳过表态首段,取后续实质内容拼接
        summary = ' '.join(clean_parts[1:4])
        if len(summary) <= max_chars:
            return summary
        return _truncate_at_sentence(summary, max_chars)

    # 检测首段是否为重要新闻导语(即使没有典型action关键词)
    # 特征:包含具体日期+重要事件+机构/人物
    # 修复(2026-06-29): 新增"投运/通车/通航/竣工/交付/揭牌"等基础设施/工程类导语关键词
    is_important_lead = bool(re.search(r'\d{1,2}月\d{1,2}日.*?(研讨会|大会|会议|论坛|峰会|启动|签约|成立|揭牌|投产|投运|通车|通航|竣工|交付|发布|举行)', first_para))

    if (first_para_raw_len > 80 and ((has_action or has_data) and not is_narrative)) or is_important_lead:
        # 倒金字塔结构,首段即摘要
        # 修复(2026-06-17): 以冒号结尾的首段,拼接后续内容
        if ends_with_colon and len(clean_parts) > 1:
            summary = first_para + ' '.join(clean_parts[1:4])
            if len(summary) <= max_chars:
                return summary
            return _truncate_at_sentence(summary, max_chars)
        # 修复(2026-06-24): 次段以冒号结尾的预告句,也需拼接后续内容(如"从六方面提出具体举措:")
        if second_ends_with_colon and len(clean_parts) > 2:
            summary = first_para + ' ' + clean_parts[1] + ' '.join(clean_parts[2:8])
            if len(summary) <= max_chars:
                return summary
            return _truncate_at_sentence(summary, max_chars)
        # 修复(2026-06-17): 重要导语但首段过短(<80字),说明导语被切分,需拼接后续内容
        if is_important_lead and first_para_raw_len < 80 and len(clean_parts) > 1:
            summary = first_para + ' '.join(clean_parts[1:6])  # 增加拼接范围(央广网6项政策)
            if len(summary) <= max_chars:
                return summary
            return _truncate_at_sentence(summary, max_chars)
        if len(first_para) <= max_chars:
            return first_para
        else:
            # 首段过长,截断到max_chars
            return _truncate_at_sentence(first_para, max_chars)

    # 3. 结构复杂/重点后置:首段太水或太短,取首段+后续段落拼接
    if len(clean_parts) > 1:
        # 修复(2026-07-02): 不要硬编码4段上限,取所有段落直到max_chars
        # 过滤掉<=10字的短段(小标题如"快速与缓慢"),避免浪费空间
        meaningful = [p for p in clean_parts if len(p) > 10]
        if not meaningful:
            meaningful = clean_parts
        # 短首段(<=80字)通常是导语,先拼上它再加后续所有有意义段落
        if first_para_raw_len <= 80:
            summary = ' '.join(meaningful)
        else:
            # 长首段,跳过头段取后续
            summary = ' '.join(meaningful[1:]) if len(meaningful) > 1 else meaningful[0]
        if len(summary) <= max_chars:
            return summary
        return _truncate_at_sentence(summary, max_chars)

    # 4. 兜底:只有一段且不长
    return _truncate_at_sentence(first_para, max_chars)


def _clean_tail_datelines(text):
    """兜底清理:去除文本末尾的尾部电头署名(如"本报雄安电" "本报拉萨7月7日电")"""
    if not text:
        return text
    # 模式: 本报/XX报 + 1-8字地点 + 电(可选日期) + 结尾
    # 例: "本报雄安电" "本报拉萨7月7日电" "经济日报雄安电"
    text = re.sub(r'\s*(?:本报|[\u4e00-\u9fa5]+报)[\u4e00-\u9fa5\d月日]{1,15}电\s*$', '', text)
    return text.strip()


def _truncate_at_sentence(text, max_chars):
    """在max_chars范围内截断,优先保留完整句子"""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    # 找最近的句号/叹号/问号/右括号
    last_period = max(
        truncated.rfind('。'),
        truncated.rfind('!'),
        truncated.rfind('?'),
        truncated.rfind(')'),
        truncated.rfind(')'),
    )
    if last_period > max_chars * 0.5:
        return truncated[:last_period + 1]
    return truncated + '......'

def llm_summarize_batch(batch_news_list, batch_num, batch_total):
    """LLM 仅用于标题修复/改写(不再用于生成摘要)"""
    articles_text = ""
    needs_llm = False

    for i, n in enumerate(batch_news_list):
        content_snippet = (n.get('content', '') or n.get('summary', ''))[:800]
        raw_title = n['title']
        has_cyrillic = bool(re.search(r'[а-яА-Я]', raw_title))

        # 检测标题是否需要改写(公司仅参展/出席)
        needs_title_rewrite = bool(re.search(r'亮相|出席|参展|受邀|参加|走进|受邀参观', raw_title))
        # 但以下情况不改写
        if needs_title_rewrite and re.search(r'IPO|上市|融资|收购|合并|财报|签约|产品发布', raw_title):
            needs_title_rewrite = False

        if has_cyrillic or needs_title_rewrite:
            needs_llm = True
            if has_cyrillic:
                articles_text += f"[{i+1}] {n['source']}:(标题编码异常,请根据正文生成准确标题)\n{content_snippet}\n\n"
            else:
                articles_text += f"[{i+1}] {n['source']}:{raw_title}\n{content_snippet}\n\n"

    if not needs_llm:
        return {}  # 不需要 LLM,摘要已用原文提取

    prompt = f"""你是一个专业新闻编辑。以下新闻需要处理标题问题(摘要已另有处理,不需要你生成)。

对于每条标注为"标题编码异常"的,请根据正文生成准确的中文标题。
对于需要标题改写的(公司仅参展/出席),请将标题改为以事件为主体。

输出格式:
[编号] 来源:新标题
(不需要输出摘要)

新闻列表:
{articles_text}

请开始:"""

    response = call_llm(prompt, max_tokens=2000, temperature=0.3)
    if not response:
        print(f"  ⚠️ Batch {batch_num} LLM call failed")
        return {}

    parsed = parse_llm_response(response, len(batch_news_list))
    # 只保留 title 字段
    for k, v in parsed.items():
        parsed[k] = {'title': v.get('title', ''), 'summary': ''}
    return parsed

def llm_batch_summarize(news_list):
    """从新闻原文提取关键内容作为摘要(不再用 LLM 改写)

    流程:
    1. 对每条新闻,从 content 字段提取原文关键段落作为摘要
    2. 仅对标题编码异常/需要改写的新闻调用 LLM(只处理标题,不生成摘要)
    """
    if len(news_list) == 0:
        return []

    # 检测需要 LLM 处理标题的新闻
    title_fix_indices = set()
    for i, news in enumerate(news_list):
        raw_title = news['title']
        has_cyrillic = bool(re.search(r'[а-яА-Я]', raw_title))
        # 检测标题是否需要改写(公司仅参展/出席)
        needs_title_rewrite = bool(re.search(r'亮相|出席|参展|受邀|参加|走进|受邀参观', raw_title))
        # 但以下情况不改写
        if needs_title_rewrite and re.search(r'IPO|上市|融资|收购|合并|财报|签约|产品发布', raw_title):
            needs_title_rewrite = False

        if has_cyrillic or needs_title_rewrite:
            title_fix_indices.add(i)

    start = time.time()
    extract_count = 0
    skip_count = 0

    # 1) 先用原文提取给所有新闻生成摘要
    for i, news in enumerate(news_list):
        content_raw = news.get('content', '') or ''
        summary_raw = news.get('summary', '') or ''
        # 修复(2026-06-25): 换行符/全角空格差异导致去重失败
        # 归一化:全角空格→半角空格,换行→空格,再进行去重判断
        # 修复(2026-07-08): 连续空格也归一化,避免"XX电  （"vs"XX电 （"导致去重失败
        content_norm = re.sub(r'\s+', ' ', content_raw.replace('\u3000', ' ').replace('\r', '').replace('\n', ' ').strip())
        summary_norm = re.sub(r'\s+', ' ', summary_raw.replace('\u3000', ' ').replace('\r', '').replace('\n', ' ').strip())
        # 去重:如果 content 和 summary 相同(或互为子串),只取较长者,避免拼接重复
        if content_raw and summary_raw:
            if content_raw == summary_raw or content_norm == summary_norm or content_raw in summary_raw or summary_raw in content_raw or content_norm in summary_norm or summary_norm in content_norm:
                content = content_raw if len(content_raw) >= len(summary_raw) else summary_raw
            else:
                content = content_raw + summary_raw
        else:
            content = content_raw + summary_raw

        if len(content.strip()) < 30:
            # 原文太短,用 title 作为摘要
            news['summary'] = news.get('title', '')
            skip_count += 1
            continue

        # 从原文提取
        summary = extract_original_summary(content, news['title'])
        # 修复(2026-07-08): 兜底清理摘要末尾的尾部电头署名(如"本报雄安电" "本报拉萨7月7日电")
        if summary:
            summary = re.sub(r'\s*(?:本报|[\u4e00-\u9fa5]+报)[\u4e00-\u9fa5\d月日]{1,15}电\s*$', '', summary).strip()
            summary = re.sub(r'\s*(?:责任编辑[::][^）)]*|[\uff08(]责任编辑[\uff09)][^）)]*|[\uff08(]责编[^\uff09)]*[\uff09)]|[\uff08(]编辑[^\uff09)]*[\uff09)]|[\uff08(]文案[^\uff09)]*[\uff09)])\s*$', '', summary).strip()
            # 再次清理(可能在编辑信息后面还有电头)
            summary = re.sub(r'\s*(?:本报|[\u4e00-\u9fa5]+报)[\u4e00-\u9fa5\d月日]{1,15}电\s*$', '', summary).strip()
        if summary:
            news['summary'] = summary
            extract_count += 1
        else:
            # 提取失败,用原 summary 或 title
            news['summary'] = news.get('summary', '') or news.get('title', '')
            skip_count += 1

    if extract_count > 0:
        print(f"  ✅ 原文提取摘要: {extract_count}/{len(news_list)} 条")
    if skip_count > 0:
        print(f"  ⚠️ 跳过(原文不足): {skip_count}/{len(news_list)} 条")

    # 2) 对需要标题修复的新闻调用 LLM
    if title_fix_indices:
        print(f"  📝 {len(title_fix_indices)} 条新闻需要标题修复/改写,调用 LLM...")

        title_fix_news = [(i, news_list[i]) for i in sorted(title_fix_indices)]
        articles_per_batch = 8
        batches = []
        for i in range(0, len(title_fix_news), articles_per_batch):
            batches.append(title_fix_news[i:i + articles_per_batch])

        for batch_idx, batch in enumerate(batches):
            if len(batch) == 0:
                continue

            batch_news = [n for _, n in batch]

            max_retries = 3
            for attempt in range(max_retries):
                try:
                    summaries = llm_summarize_batch(batch_news, batch_idx+1, len(batches))
                    if summaries:
                        break
                    if attempt < max_retries - 1:
                        wait_time = 30 * (attempt + 1)
                        print(f"  ⚠️ Batch {batch_idx+1} returned empty, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                except Exception as e:
                    if attempt < max_retries - 1:
                        wait_time = 30 * (attempt + 1)
                        print(f"  ⚠️ Batch {batch_idx+1} error: {e}, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"  ❌ Batch {batch_idx+1} failed after {max_retries} retries: {e}")
                        summaries = {}

            # 更新标题(摘要不变)
            for local_idx, data in summaries.items():
                if data.get('title'):
                    orig_idx = batch[local_idx - 1][0]
                    old_title = news_list[orig_idx]['title']
                    news_list[orig_idx]['title'] = data['title']
                    print(f"    📝 标题修复: {old_title[:40]}... → {data['title'][:40]}...")

            if batch_idx < len(batches) - 1:
                print(f"  ⏳ Waiting 20s before next batch...")
                time.sleep(20)

    elapsed = time.time() - start
    print(f"  ✅ 摘要生成完成: {extract_count}/{len(news_list)} 条原文提取, 耗时 {elapsed:.1f}s")

    return news_list

def main():
    """Main flow"""
    print(f"\n{'='*60}")
    print(f"  Stage 2.5: LLM Batch Summary")
    print(f"{'='*60}\n")

    start = time.time()

    # 1. Init digest_output table
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS digest_output (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            source TEXT NOT NULL,
            publish_date TEXT NOT NULL,
            summary TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            keywords TEXT,
            digest_date TEXT NOT NULL,
            source_article_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    # 1.5 Clear stale records from today (previous runs on the same day)
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute("DELETE FROM digest_output WHERE digest_date = ?", (today,))
    cleared = c.rowcount
    conn.commit()
    if cleared > 0:
        print(f"  [清理] 清除今天旧的 digest_output 记录 {cleared} 条")

    # 2. Query ALL eligible articles (exclude any url already in digest_output)
    # 动态日期窗口:默认今天+昨天(2天),周末/假期扩到3天,不足则加到7天
    _now = datetime.now()
    dow = _now.weekday()  # 0=周一, 6=周日
    if dow >= 5:  # 周六(5)或周日(6)
        initial_days = 3
    else:
        initial_days = 2

    def _count_eligible(df):
        """快速统计某日期窗口内的候选文章数
        排除:已去重、已有 digest_output、FGB 已采用(matched_article_id IS NOT NULL)"""
        c2 = conn.cursor()
        c2.execute('''
            SELECT COUNT(*) FROM articles a
            WHERE a.publish_date >= ?
            AND a.is_duplicate = 0
            AND a.url NOT IN (SELECT url FROM digest_output)
            AND a.content IS NOT NULL
            AND LENGTH(a.content) > 30
            AND a.title NOT LIKE '%百问百答%'
            AND a.title NOT LIKE '%编辑手记%'
            AND a.source != '人民日报主站'
            AND a.title NOT LIKE '%学习新语%'
            AND a.title NOT LIKE '%习言道%'
            AND a.title NOT LIKE '%学习·知行%'
            AND a.url NOT LIKE 'fgb://%'
            AND a.id NOT IN (SELECT matched_article_id FROM fgb_broadcast WHERE matched_article_id IS NOT NULL)
        ''', (df,))
        return c2.fetchone()[0]

    date_from = (_now - timedelta(days=initial_days)).strftime('%Y-%m-%d')
    count = _count_eligible(date_from)
    if count < 10:
        print(f"  [窗口扩展] 初始窗口({initial_days}天)仅 {count} 条 < 10,扩展到 7 天")
        date_from = (_now - timedelta(days=7)).strftime('%Y-%m-%d')
    else:
        print(f"  [日期窗口] {initial_days} 天({date_from} ~ {today}),候选 {count} 条")

    c.execute('''
        SELECT a.id, a.title, a.source, a.publish_date, a.summary, a.url, a.keywords, a.content
        FROM articles a
        WHERE a.publish_date >= ?
        AND a.is_duplicate = 0
        AND a.url NOT IN (SELECT url FROM digest_output)
        AND a.content IS NOT NULL
        AND LENGTH(a.content) > 30
        AND a.title NOT LIKE '%百问百答%'
        AND a.title NOT LIKE '%编辑手记%'
        AND a.source != '人民日报主站'
        AND a.title NOT LIKE '%学习新语%'
        AND a.title NOT LIKE '%习言道%'
        AND a.title NOT LIKE '%学习·知行%'
        AND a.url NOT LIKE 'fgb://%'
        AND a.id NOT IN (SELECT matched_article_id FROM fgb_broadcast WHERE matched_article_id IS NOT NULL)
        ORDER BY a.id DESC
    ''', (date_from,))

    all_rows = c.fetchall()
    all_news = []
    for row in all_rows:
        all_news.append({
            'id': row[0], 'title': row[1], 'source': row[2],
            'publish_date': row[3], 'summary': row[4],
            'url': row[5], 'keywords': row[6], 'content': row[7]
        })

    # === 低质量内容过滤 ===
    # 注意:不是砍短内容,而是过滤质量低、旧闻、无增量的内容
    # 1. 每日例行数据(央行逆回购、汇率中间价等,每天发无增量)
    # 2. 内容过短(只有标题/1-2句话,无实质正文)
    # 3. 非核心社会事件(食物中毒、交通事故等)
    # 4. 主体内容不足(例行发布会表态,无实质新信息)
    skip_title_keywords = [
        # 每日例行数据
        r'逆回购操作', r'中间价报', r'人民币汇率中间价',
        r'银行间外汇市场', r'中国人民银行授权',
        # 非核心社会事件
        r'食用.*中毒', r'交通事故',
    ]
    min_content_length = 100  # 修复(2026-07-08): 150→100，国标发布/AI增速/氢供应链等短讯有实质价值

    # 企业公关/赞助内容过滤(标题+内容)
    corporate_pr_keywords = [
        r'捐赠', r'赞助', r'战略合作', r'深度联动',
        r'进驻.*奥体', r'进驻.*体育中心',
        r'体育.*健康.*融合', r'筑牢健康防线',
        # 企业声明/报警/公关回应(非产业新闻)
        r'针对我司报警', r'针对.*报警的声明',
        # 汽车品牌软文/品牌宣传长文(非产业动态/非政策)
        r'跑出确定性', r'交出.*答卷', r'品牌发布以来',
        r'用户型科技', r'穿越.*周期', r'体系.*能力',
    ]

    # 国际地缘政治/军事冲突过滤(标题)
    geopol_keywords = [
        r'谅解备忘录', r'霍尔木兹海峡', r'海上封锁',
        r'军事打击', r'美伊',
        # 外国政治人物/选举/就任(非中国产业/科技/经济)
        r'宣誓就任.*总统', r'就任秘鲁',
    ]

    # 宣传/评论栏目过滤(标题)
    propaganda_keywords = [
        r'绘说现代化', r'绘说', r'零时差', r'与其炒作',
    ]

    # 银行PR/金融服务宣传(非产业动态)
    bank_pr_keywords = [
        r'赋能.*文旅', r'赋能.*海上', r'助老连心桥', r'养老集市',
        r'蓝色专项授信', r'专项金融服务方案', r'量身定制.*金融',
        r'智慧收单', r'资金归集', r'一站式结算',
        r'精准对接需求', r'破解融资难题', r'创新授信模式',
        r'配套综合服务', r'筑牢.*根基', r'传递金融温度',
        r'该行主动走访调研', r'授信准入', r'增信依据',
    ]

    # 地方招商/经开区/高新区宣传
    local_promotion_keywords = [
        r'经开区.*聚链', r'高新区.*落地', r'经开区.*新动能',
        r'产业园.*投产', r'产业园.*建设', r'产业园.*进展',
        r'厚植.*热土', r'打造.*高地', r'招商.*引资',
        r'企业聚链成群', r'葡萄串.*效应',
        r'小灯塔.*企业', r'链主.*企业',
        r'加快推进.*项目', r'取得.*进展',
    ]

    # 软性专栏/调研行(非硬新闻)
    soft_column_keywords = [
        r'活力中国调研行', r'尺素金声', r'一线见闻',
        r'调研行.*看', r'调研行.*走进', r'看大国',
        r'美丽中国行', r'在希望的田野上', r'新闻联播',
        r'探馆', r'探访.*馆', r'走进.*馆',
        r'从四个趋势透视', r'经济观察',
        r'从.*数据看', r'数据看懂',
        # 修复(2026-07-24): 人文特写/个人故事/乡村振兴故事(非产业/科技/经济)
        r'的故事$', r'村里来了',
    ]

    # 生态/野生动物繁育故事(非政策/产业价值)
    nature_wildlife_keywords = [
        r'扬子鳄', r'大熊猫.*产.*卵', r'大熊猫.*繁育',
        r'野生动物.*繁育', r'自然保护区.*迎来',
        r'野生动物.*产.*崽', r'珍稀动物.*繁殖',
        r'生态.*监护', r'红外相机.*记录',
    ]

    # 不需要出现在摘要中的主题
    skip_topic_keywords = [
        # 血液调配数据(例行统计,无增量)
        r'调配血液', r'无偿献血.*单位',
        # 军事/航母(非产业新闻)
        r'航母编队', r'甩掉偷窥者',
        # 游泳/体育比赛(名单/成绩类非产业)
        r'游泳队.*参赛名单', r'亚运会.*名单',
        # 体育赛事/比赛/活动(通用,非产业新闻)
        r'菁英赛', r'精英赛', r'公开赛', r'邀请赛',
        r'总决赛', r'冠军赛', r'选拔赛',
        r'运动会$', r'体育节', r'全民健身',
        r'马拉松', r'越野赛', r'搏击', r'拳赛',
        r'格斗', r'演唱会', r'音乐节', r'巡演',
        r'文艺汇演', r'晚会',
        # 足球/篮球/乒乓球等体育赛事(非产业)
        r'足球.*赛', r'篮球.*赛', r'乒乓球.*赛',
        r'羽毛球.*赛', r'网球.*赛', r'田径.*赛',
        r'游泳.*赛', r'体操', r'骑行',
        # 体育赛事邀请/文化交流活动(村超等,非产业新闻)
        r'村超.*邀请赛', r'村超.*邀请',
        r'以足球为媒', r'体育赛事.*邀请',
        # 地方性/青少年体育赛事(非产业)
        r'青少年足球', r'青少年体育.*菁英赛',
        r'青少年.*足球.*菁英', r'青少年.*篮球',
        r'青少年.*锦标赛', r'青少年.*运动会',
        r'校园足球', r'校园.*体育比赛',
        r'中小学生.*运动会', r'中学生.*运动会',
        r'中小学生.*体育', r'青少年.*比赛',
        r'青少年.*赛$', r'校园.*联赛',
        r'联合会杯.*青少年', r'青少年.*联赛',
        r'青少年俱乐部', r'青少年.*锦标赛$',
        # 酒类/食品市场整治/食品安全专项执法/消费者打假曝光(非产业/科技)
        r'净化.*酒类市场', r'酒类.*专项整', r'两超一非',
        r'捣毁.*制假售假', r'酒类产品.*抽检',
        r'鲜榨.*鲜诈', r'鲜榨.*勾兑', r'NFC.*鲜榨',
        r'暗访.*代工厂', r'100%鲜榨',
        # 华尔街股市评论/多空观点交锋(非产业新闻)
        r'华尔街.*牛市', r'华尔街.*对立观点', r'华尔街.*交锋',
        r'盈利泡沫', r'美股.*高估', r'市盈率.*泡沫',
        r'多空阵营', r'标普500.*市盈率',
        # 革命文物保护/党建基层宣传(非产业/科技/经济)
        r'革命文物', r'党旗.*基层', r'抵边.*社区',
        r'边疆.*党建', r'全国先进基层党组织',
        # 论坛峰会类活动(无实质产业信息)
        r'论坛.*启幕', r'揭牌仪式.*论坛', r'CEO.*论坛',
        # 地方性文体活动/群众体育赛事(非产业)
        r'群众.*运动会', r'全民健身.*活动',
        r'广场舞', r'健身舞比赛',
        r'社区运动会', r'街道运动会',
    ]

    filtered_news = []
    skipped_reasons = []
    for n in all_news:
        title = n['title']
        content = n.get('content', '') or ''
        skip = False

        # 规则0: 企业公关/赞助
        text = title + ' ' + (content or '')
        for kw in corporate_pr_keywords:
            if re.search(kw, text):
                skip = True
                skipped_reasons.append(f"[公关] {title[:40]}")
                break

        # 规则0d: 银行PR
        if not skip:
            for kw in bank_pr_keywords:
                if re.search(kw, text):
                    skip = True
                    skipped_reasons.append(f"[银行PR] {title[:40]}")
                    break

        # 规则0e: 地方招商/经开区宣传（仅过滤市/县/区级具体项目）
        # 修复(2026-07-08): 不用白名单模式，改用"政策层级"判断
        # 省级及以上政策 → 放行；市级/区/县级产业园/招商 → 过滤
        if not skip:
            provincial_or_above = re.search(
                r'(省|国务院|国家发展|国家发改|工信部|商务部|财政部|人民银行|'
                r'中共中央|全国人大|政协全国|海关总署|税务总局|市场监管总局|'
                r'自然资源部|生态环境部|住房城乡建设|交通运输|水利部|'
                r'农业农村|文化和旅游|卫生健康|应急管理|审计署)',
                title + ' ' + (content or '')[:200]
            )
            if provincial_or_above:
                pass  # 省级及以上政策，跳过地方招商过滤
            else:
                for kw in local_promotion_keywords:
                    if re.search(kw, text):
                        skip = True
                        skipped_reasons.append(f"[地方招商] {title[:40]}")
                        break

        # 规则0f: 软性专栏
        if not skip:
            for kw in soft_column_keywords:
                if re.search(kw, title):
                    skip = True
                    skipped_reasons.append(f"[软专栏] {title[:40]}")
                    break

        # 规则0g: 生态/野生动物繁育故事
        if not skip:
            for kw in nature_wildlife_keywords:
                if re.search(kw, text):
                    skip = True
                    skipped_reasons.append(f"[生态故事] {title[:40]}")
                    break

        # 规则0h: 不需要的主题(血液调配/航母/体育名单)
        if not skip:
            for kw in skip_topic_keywords:
                if re.search(kw, title):
                    skip = True
                    skipped_reasons.append(f"[不需要] {title[:40]}")
                    break

        # 规则1: 每日例行数据(每天发,无增量价值)
        for kw in skip_title_keywords:
            if re.search(kw, title):
                skip = True
                skipped_reasons.append(f"[例行] {title[:40]}")
                break

        # 规则2: 内容过短(标题级新闻,无实质正文)
        if not skip and len(content.strip()) < min_content_length:
            skip = True
            skipped_reasons.append(f"[短] {title[:40]}")

        if skip:
            continue
        filtered_news.append(n)

    if skipped_reasons:
        print(f"  [低质量过滤] 过滤 {len(skipped_reasons)} 条:")
        for r in skipped_reasons:
            print(f"    {r}")
    all_news = filtered_news

    if len(all_news) == 0:
        print("  No new articles to summarize (or all done)")
        conn.close()
        return 0

    print(f"  Total eligible articles: {len(all_news)}")

    # Apply authoritative priority: each authoritative source gets at least min_per_authoritative
    authoritative_sources = [
        '人民网', '新华网', '新华社', '人民日报',
        '央广网', '经济日报', '科技日报', '科学网',
        '中国科技网', '科创版日报', '中国经济网'
    ]
    min_per_authoritative = 2
    max_count = 60  # 与 MAX_OUTPUT_COUNT 一致

    # 非核心源降级(36氪等低质量内容最后才选)
    low_priority_sources = ['36 氪', '中宏网']

    if len(all_news) > max_count:
        # Group by source
        by_source = {}
        for n in all_news:
            src = n['source']
            if src not in by_source:
                by_source[src] = []
            by_source[src].append(n)

        # Select authoritative sources first (at least 2 each)
        selected_ids = set()
        selected = []
        for src in authoritative_sources:
            if src in by_source:
                articles = sorted(by_source[src], key=lambda x: x['id'], reverse=True)
                for a in articles[:min_per_authoritative]:
                    if a['id'] not in selected_ids:
                        selected.append(a)
                        selected_ids.add(a['id'])

        # Fill remaining by ID descending (excluding low-priority sources)
        remaining = [n for n in all_news if n['id'] not in selected_ids and n['source'] not in low_priority_sources]
        remaining.sort(key=lambda x: x['id'], reverse=True)

        for n in remaining:
            if len(selected) >= max_count:
                break
            selected.append(n)
            selected_ids.add(n['id'])

        # 如果还有空位,才选非核心源
        if len(selected) < max_count:
            low_remaining = [n for n in all_news if n['id'] not in selected_ids]
            low_remaining.sort(key=lambda x: x['id'], reverse=True)
            for n in low_remaining:
                if len(selected) >= max_count:
                    break
                selected.append(n)
                selected_ids.add(n['id'])

        news_list = selected[:max_count]
        auth_count = sum(1 for n in news_list if n['source'] in authoritative_sources)
        print(f"  Articles to summarize: {len(news_list)} (authoritative priority applied, {auth_count} from authoritative sources)")
    else:
        news_list = all_news
        print(f"  Articles to summarize: {len(news_list)} (all eligible)")

    # 2.5 跨天标题去重(在 LLM 之前,不浪费 token)
    # 注意:url 重复已在 SQL 层排除,此处仅拦截 url 不同但标题高度相似的文章
    try:
        from .config import CROSS_DAY_DEDUP_ENABLED
        if CROSS_DAY_DEDUP_ENABLED:
            from .cross_day_dedup import filter_cross_day_duplicates
            print(f"\n  [跨天标题去重] 检查最近历史摘要(标题相似度,url 已在 SQL 层排除)...")
            news_list, blocked = filter_cross_day_duplicates(news_list, verbose=True)
            if blocked:
                print(f"  [跨天标题去重] 保留 {len(news_list)} 条,标题拦截 {len(blocked)} 条\n")
            else:
                print(f"  [跨天标题去重] 保留 {len(news_list)} 条,无标题拦截\n")
    except ImportError:
        pass

    # === 低质量内容过滤 ===
    # 过滤规则(不是因为短不要,而是因为质量低或旧闻):
    # 0. 企业公关/赞助、国际地缘政治、宣传评论
    # 1. 每日例行数据(央行逆回购、汇率中间价等,每天发无增量)
    # 2. 内容过短(只有标题/1-2句话,无实质正文)
    # 3. 非核心社会事件(食物中毒、交通事故等)
    # 4. 主体内容不足(例行发布会表态,无实质新信息)
    skip_title_keywords = [
        # 每日例行数据
        r'逆回购操作', r'中间价报', r'人民币汇率中间价',
        r'银行间外汇市场', r'中国人民银行授权',
        # 非核心社会事件
        r'食用.*中毒', r'交通事故',
    ]
    min_content_length = 100  # 修复(2026-07-08): 150→100

    # 企业公关/赞助内容过滤(标题+内容)
    corporate_pr_keywords = [
        r'捐赠', r'赞助', r'战略合作', r'深度联动',
        r'进驻.*奥体', r'进驻.*体育中心',
        r'体育.*健康.*融合', r'筑牢健康防线',
        # 企业声明/报警/公关回应(非产业新闻)
        r'针对我司报警', r'针对.*报警的声明',
        # 汽车品牌软文/品牌宣传长文(非产业动态/非政策)
        r'跑出确定性', r'交出.*答卷', r'品牌发布以来',
        r'用户型科技', r'穿越.*周期', r'体系.*能力',
    ]

    # 国际地缘政治/军事冲突过滤(标题)
    geopol_keywords = [
        r'谅解备忘录', r'霍尔木兹海峡', r'海上封锁',
        r'军事打击', r'美伊',
        # 外国政治人物/选举/就任(非中国产业/科技/经济)
        r'宣誓就任.*总统', r'就任秘鲁',
    ]

    # 宣传/评论栏目过滤(标题)
    propaganda_keywords = [
        r'绘说现代化', r'绘说', r'零时差', r'与其炒作',
    ]

    # 银行PR/金融服务宣传(非产业动态)
    bank_pr_keywords = [
        r'赋能.*文旅', r'赋能.*海上', r'助老连心桥', r'养老集市',
        r'蓝色专项授信', r'专项金融服务方案', r'量身定制.*金融',
        r'智慧收单', r'资金归集', r'一站式结算',
        r'精准对接需求', r'破解融资难题', r'创新授信模式',
        r'配套综合服务', r'筑牢.*根基', r'传递金融温度',
        r'该行主动走访调研', r'授信准入', r'增信依据',
    ]

    # 地方招商/经开区/高新区宣传
    local_promotion_keywords = [
        r'经开区.*聚链', r'高新区.*落地', r'经开区.*新动能',
        r'产业园.*投产', r'产业园.*建设', r'产业园.*进展',
        r'厚植.*热土', r'打造.*高地', r'招商.*引资',
        r'企业聚链成群', r'葡萄串.*效应',
        r'小灯塔.*企业', r'链主.*企业',
        r'加快推进.*项目', r'取得.*进展',
    ]

    # 软性专栏/调研行(非硬新闻)
    soft_column_keywords = [
        r'活力中国调研行', r'尺素金声', r'一线见闻',
        r'调研行.*看', r'调研行.*走进', r'看大国',
        r'美丽中国行', r'在希望的田野上', r'新闻联播',
        r'探馆', r'探访.*馆', r'走进.*馆',
        r'从四个趋势透视', r'经济观察',
        r'从.*数据看', r'数据看懂',
        # 修复(2026-07-24): 人文特写/个人故事/乡村振兴故事(非产业/科技/经济)
        r'的故事$', r'村里来了',
    ]

    filtered_news = []
    skipped_reasons = []
    for n in news_list:
        title = n['title']
        content = n.get('content', '') or ''
        skip = False

        # 规则0: 企业公关/赞助
        text = title + ' ' + (content or '')
        for kw in corporate_pr_keywords:
            if re.search(kw, text):
                skip = True
                skipped_reasons.append(f"[公关] {title[:40]}")
                break

        # 规则0b: 国际地缘政治
        if not skip:
            for kw in geopol_keywords:
                if re.search(kw, title):
                    skip = True
                    skipped_reasons.append(f"[地缘] {title[:40]}")
                    break

        # 规则0c: 宣传/评论栏目
        if not skip:
            for kw in propaganda_keywords:
                if re.search(kw, title):
                    skip = True
                    skipped_reasons.append(f"[宣传] {title[:40]}")
                    break

        # 规则0d: 银行PR
        if not skip:
            for kw in bank_pr_keywords:
                if re.search(kw, text):
                    skip = True
                    skipped_reasons.append(f"[银行PR] {title[:40]}")
                    break

        # 规则0e: 地方招商/经开区宣传（仅过滤市/县/区级具体项目）
        # 修复(2026-07-08): 不用白名单模式，改用"政策层级"判断
        # 省级及以上政策 → 放行；市级/区/县级产业园/招商 → 过滤
        if not skip:
            provincial_or_above = re.search(
                r'(省|国务院|国家发展|国家发改|工信部|商务部|财政部|人民银行|'
                r'中共中央|全国人大|政协全国|海关总署|税务总局|市场监管总局|'
                r'自然资源部|生态环境部|住房城乡建设|交通运输|水利部|'
                r'农业农村|文化和旅游|卫生健康|应急管理|审计署)',
                title + ' ' + (content or '')[:200]
            )
            if provincial_or_above:
                pass  # 省级及以上政策，跳过地方招商过滤
            else:
                for kw in local_promotion_keywords:
                    if re.search(kw, text):
                        skip = True
                        skipped_reasons.append(f"[地方招商] {title[:40]}")
                        break

        # 规则0f: 软性专栏
        if not skip:
            for kw in soft_column_keywords:
                if re.search(kw, title):
                    skip = True
                    skipped_reasons.append(f"[软专栏] {title[:40]}")
                    break

        # 规则1: 每日例行数据(每天发,无增量价值)
        for kw in skip_title_keywords:
            if re.search(kw, title):
                skip = True
                skipped_reasons.append(f"[例行] {title[:40]}")
                break

        # 规则2: 内容过短(标题级新闻,无实质正文)
        if not skip and len(content.strip()) < min_content_length:
            skip = True
            skipped_reasons.append(f"[短] {title[:40]}")

        if skip:
            continue
        filtered_news.append(n)

    if skipped_reasons:
        print(f"  [低质量过滤] 过滤 {len(skipped_reasons)} 条:")
        for r in skipped_reasons:
            print(f"    {r}")
    news_list = filtered_news

    # === 同一主题去重 ===
    # 同一事件/主题只保留信息量最大的一条(按content长度判断)
    def topic_dedup(nl):
        topic_map = {}
        for n in nl:
            title = n['title']
            content = n.get('content', '') or ''
            topic = None

            # === 统计局数据类同主题去重 ===
            # 同一统计局数据,多个来源(人民网/经济日报/中宏网/科技日报等)重复发布
            stats_patterns = {
                '统计局_1-5月国民经济': ['1.5月.*国民经济', '1-5月.*国民经济', '前5个月.*国民经济'],
                '统计局_5月工业生产': ['5月份.*规模以上工业.*增长', '5月工业.*增长'],
                '统计局_1-5月固投': ['1.5月.*固定资产.*投资', '1-5月.*固定.*投资'],
                '统计局_1-5月社消零': ['1.5月.*社会消费品.*零售', '1-5月.*社消.*零售'],
                '统计局_1-5月房地产': ['1.5月.*房地产.*投资', '1-5月.*房地产.*投资'],
                '统计局_5月能源生产': ['5月.*能源生产'],
                '统计局_5月原煤': ['5月.*原煤.*产量', '1.5月.*原煤产量'],
                '统计局_一二三线城市房价': ['一二三线城市.*商品住宅.*销售价格', '一二三线城市.*房价'],
                '统计局_规上工业利润': ['规上工业.*利润总额', '规模以上工业.*利润'],
            }
            if not topic:
                for tname, patterns in stats_patterns.items():
                    for pat in patterns:
                        if re.search(pat, title):
                            topic = tname
                            break
                    if topic:
                        break

            # === 硬编码主题 ===
            if not topic:
                if 'SpaceX' in title or 'SpaceX' in content:
                    topic = 'SpaceX_IPO'
                elif '脑机接口' in title:
                    topic = '脑机接口'

            # === 政策文件跨天去重 ===
            # 同一政策文件/数据,不同来源/不同天重复发布,只保留内容最丰富的一条
            policy_patterns = {
                '平台经济大中小企业协同': [
                    '平台经济.*大中小企业.*协同',
                    '大中小企业.*融通.*七部门',
                    '促进平台经济大中小企业协同发展',
                ],
                '海洋经济就业创业': [
                    '海洋经济.*就业创业',
                    '海洋经济.*稳岗扩容',
                    '支持海洋经济发展.*通知',
                ],
                '国家铁路货运数据': [
                    '国家铁路.*货物.*亿吨',
                    '前\d+月国家铁路发送货物',
                    '1至\d+月.*国家铁路.*货物',
                ],
            }
            if not topic:
                for tname, patterns in policy_patterns.items():
                    for pat in patterns:
                        if re.search(pat, title):
                            topic = tname
                            break
                    if topic:
                        break

            if topic:
                if topic not in topic_map:
                    topic_map[topic] = []
                topic_map[topic].append((len(content), n))

        kept_ids = set()
        removed_titles = []
        for topic, items in topic_map.items():
            # 统计局数据类:优先保留人民网/经济日报/新华网,排除中宏网/科技日报的简单转发
            priority_sources = ['人民网', '经济日报', '新华网', '央广网']
            items.sort(key=lambda x: (
                1 if any(s in x[1].get('source', '') for s in priority_sources) else 0,
                x[0]  # 其次按content长度
            ), reverse=True)
            kept_ids.add(items[0][1]['id'])
            for _, n in items[1:]:
                removed_titles.append(n)

        if removed_titles:
            print(f"  [主题去重] 过滤 {len(removed_titles)} 条重复主题:")
            for n in removed_titles:
                print(f"    ✂ {n['source']}: {n['title'][:50]}")

        removed_ids = {r['id'] for r in removed_titles}
        return [n for n in nl if n['id'] in kept_ids or n['id'] not in removed_ids]

    news_list = topic_dedup(news_list)

    # 3. LLM Summary
    news_list = llm_batch_summarize(news_list)

    # 4. Save to digest_output
    saved = 0
    for news in news_list:
        try:
            c.execute('''
                INSERT OR IGNORE INTO digest_output
                (title, source, publish_date, summary, url, keywords, digest_date, source_article_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                news['title'], news['source'], news['publish_date'],
                news['summary'], news['url'], news.get('keywords', ''),
                today, news['id']
            ))
            if c.rowcount > 0:
                saved += 1
        except Exception as e:
            print(f"  Save failed: {news['title'][:30]}... - {e}")

    conn.commit()
    conn.close()

    elapsed = time.time() - start
    print(f"\n  ✅ Saved {saved} articles to digest_output")
    print(f"  Total time: {elapsed:.1f}s")

    return saved

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        import traceback
        print(f"\n[ERROR] {e}")
        traceback.print_exc()
        sys.exit(1)
