# -*- coding: utf-8 -*-
"""
taxonomy.py — 骨科领域词典

把中英文混杂的自由文本归一化到标准词，撮合打分靠它对齐。
买方写 "locking plate"、卖方写 "锁定接骨板"，归一后都是「创伤」，才match得上。

用法：
  from taxonomy import norm
  norm("需要钛合金锁定板和髓内钉，要CE MDR") -> {'cat': {'创伤'}, 'material': {'钛合金'}, 'cert': {'CE MDR'}}
"""
import re

# ---------------------------------------------------------------- 词典

DOMAINS = {
    "cat": {
        "创伤": ["创伤", "trauma", "接骨板", "bone plate", "锁定板", "locking plate",
               "加压板", "重建板", "髓内钉", "intramedullary", "im nail", "股骨钉",
               "胫骨钉", "螺钉", "screw", "空心钉", "cannulated", "克氏针", "k-wire",
               "张力带", "髋部螺钉", "dhs", "外固定支架"],
        "脊柱": ["脊柱", "spine", "spinal", "椎弓根", "pedicle", "pedicle screw",
               "椎弓根螺钉", "颈椎融合器", "cervical cage", "腰椎融合", "融合器", "cage",
               "人工椎体", "vertebral", "颈椎", "cervical", "胸腰椎", "thoracolumbar",
               "前路板", "anterior plate", "后路", "posterior", "脊柱内固定", "椎间"],
        "关节": ["关节", "joint", "arthroplasty", "髋关节", "hip", "膝关节", "knee",
               "肩关节", "shoulder", "肘", "elbow", "踝", "ankle", "假体", "prosthesis",
               "股骨柄", "femoral stem", "髋臼杯", "acetabular", "衬垫", "liner",
               "髁", "condylar", "单髁", "unicondylar", "翻修", "revision"],
        "运动医学": ["运动医学", "sports medicine", "sports med", "缝合锚钉", "suture anchor",
                 "带线锚钉", "anchor",
                 "半月板", "meniscus", "韧带", "ligament", "acl", "pcl", "交叉韧带",
                 "带袢", "endobutton", "袢板", "肌腱", "tendon", "肩袖", "rotator cuff",
                 "半月板缝合", "半月板修复"],
        "外固定": ["外固定", "external fixation", "external fixator", "ilizarov",
                "伊利扎诺夫", "环形支架", "单边支架", "骨延长", "bone transport"],
        "骨修复材料": ["骨修复", "bone graft", "骨填充", "bone void", "骨移植", "人工骨",
                  "骨水泥", "bone cement", "pmma", "羟基磷灰石", "磷酸钙", "calcium phosphate",
                  "脱钙骨", "dbm", "骨诱导", "骨替代"],
        "手术器械": ["器械", "instrument", "动力", "power tool", "钻", "drill", "锯", "saw",
                 "磨", "burr", "骨科动力", "电动", "气动", "摆锯", "oscillating",
                 "器械盒", "instrument set", "托盘", "tray", "牵开器", "retractor",
                 "咬骨钳", "rongeur", "复位钳"],
        "一次性耗材": ["耗材", "consumable", "disposable", "一次性", "single use",
                  "敷料", "dressing", "负压引流", "冲洗", "irrigation", "骨蜡", "bone wax",
                  "止血", "hemostat", "缝合线", "手术缝线", "sutures", "手术包", "drape"],
        "支具康复": ["支具", "brace", "orthosis", "康复", "rehab", "护具", "固定带",
                 "颈托", "腰围", "walker boot", "助行", "外固定支具"],
        "兽医骨科": ["兽医", "veterinary", "vet ", "动物", "animal", "宠物", "犬", "猫",
                 "canine", "feline", "tplo"],
    },
    "process": {
        "数控加工": ["cnc", "数控", "机加工", "machining", "车削", "turning", "铣削",
                 "milling", "加工中心", "五轴", "5-axis", "精密加工"],
        "锻造": ["锻造", "forging", "锻压", "模锻", "自由锻"],
        "铸造": ["铸造", "casting", "精密铸造", "investment casting", "失蜡", "压铸"],
        "金属注射成型": ["mim", "金属注射", "metal injection", "粉末冶金", "powder metallurgy"],
        "增材制造": ["3d打印", "3d print", "增材", "additive", "slm", "ebm", "选区激光",
                 "3d printed", "快速成型"],
        "注塑": ["注塑", "injection molding", "注塑成型", "模具", "mold", "mould", "挤出",
               "extrusion"],
        "编织": ["编织", "braiding", "编织物", "weaving", "缝制", "sewing"],
        "表面处理": ["表面处理", "surface treatment", "阳极氧化", "anodizing", "anodising",
                 "喷砂", "sandblast", "grit blast", "抛光", "polishing", "电解抛光",
                 "electropolish", "涂层", "coating", "ha涂层", "等离子喷涂",
                 "plasma spray", "钝化", "passivation", "着色", "color anodize"],
        "热处理": ["热处理", "heat treatment", "固溶", "solution", "时效", "aging",
                "退火", "annealing", "淬火", "quenching"],
        "清洗包装": ["清洗", "cleaning", "超声波清洗", "包装", "packaging", "无菌包装",
                 "sterile packaging", "吸塑", "blister", "纸塑袋", "pouch", "封口",
                 "sealing", "洁净", "cleanroom", "洁净车间"],
        "灭菌": ["灭菌", "sterilization", "sterilisation", "sterile", "环氧乙烷", "eo ",
               "eto", "辐照", "irradiation", "gamma", "蒸汽灭菌", "steam", "autoclave",
               "灭菌验证", "sterilization validation"],
        "检测": ["检测", "testing", "inspection", "三坐标", "cmm", "力学测试", "mechanical test",
               "疲劳", "fatigue", "金相", "metallographic", "探伤", "ndt", "尺寸检测",
               "生物相容性", "biocompatibility", "清洁度", "cleanliness"],
        "装配": ["装配", "assembly", "组装", "组装线", "总装"],
        "激光打标": ["激光打标", "laser marking", "打标", "marking", "激光雕刻", "laser etch",
                 "udi", "二维码打标"],
    },
    "material": {
        "钛合金": ["钛合金", "titanium", "ti6al4v", "ti-6al-4v", "tc4", "gr5",
                "grade 5", "ti alloy", "钛材"],
        "纯钛": ["纯钛", "cp ti", "commercially pure titanium", "cp titanium", "gr1",
               "gr2", "grade 2", "ta2"],
        "不锈钢": ["不锈钢", "stainless steel", "316l", "316", "304", "17-4ph", "420",
                "马氏体不锈钢"],
        "钴铬钼": ["钴铬钼", "cocr", "cobalt chrome", "cobalt-chromium", "co-cr-mo",
                "钴铬", "ccm"],
        "PEEK": ["peek", "聚醚醚酮", "polyetheretherketone", "碳纤维peek", "cf/peek"],
        "超高分子量聚乙烯": ["uhmwpe", "超高分子量聚乙烯", "高分子聚乙烯", "聚乙烯",
                    "polyethylene", "交联聚乙烯", "xlpe", "highly crosslinked"],
        "可吸收材料": ["可吸收", "absorbable", "resorbable", "plla", "plga", "pga",
                  "聚乳酸", "polylactic", "镁合金", "magnesium", "可降解", "bioresorbable"],
        "生物陶瓷": ["陶瓷", "ceramic", "氧化铝", "alumina", "氧化锆", "zirconia",
                 "zta", "生物陶瓷", "bioceramic", "氮化硅", "silicon nitride"],
        "钽金属": ["钽", "tantalum", "多孔钽", "porous tantalum", "trabecular metal"],
        "羟基磷灰石": ["羟基磷灰石", "hydroxyapatite", "ha ", "磷酸钙", "calcium phosphate",
                  "tcp", "bcp", "生物活性玻璃", "bioglass"],
        "硅胶": ["硅胶", "silicone", "硅橡胶", "silicone rubber", "医用硅胶"],
        "碳纤维": ["碳纤维", "carbon fiber", "carbon fibre", "cfrp", "碳纤"],
        "钴铬钨镍": ["mp35n", "钴铬钨镍", "elgiloy", "phynox", "l-605"],
    },
    "cert": {
        "ISO 13485": ["iso13485", "iso 13485", "13485", "质量体系", "qms"],
        "FDA 510(k)": ["510k", "510(k)", "fda 510", "fda510", "510 k"],
        "FDA 注册": ["fda", "fda注册", "fda registered", "fda listing", "fda establishment"],
        "CE MDR": ["ce mdr", "mdr", "ce认证", "ce mark", "ce marked", "ce mark", "ce证书",
                 "eu mdr", "mdr ce"],
        "MDSAP": ["mdsap", "单一审核"],
        "NMPA 注册": ["nmpa", "cfda", "中国注册证", "注册证", "国械注", "三类证",
                  "二类证", "nmpa注册"],
        "GMP": ["gmp", "生产质量管理规范", "医疗器械gmp"],
        "UKCA": ["ukca", "英国", "mhra"],
        "PMDA": ["pmda", "日本", "japan", "厚生劳动省"],
        "TGA": ["tga", "澳洲", "australia"],
    },
    "market": {
        "中国": ["中国", "china", "国内", "domestic", "大陆"],
        "美国": ["美国", "usa", "u.s.", "united states", "北美", "north america",
               "北美市场", "us"],
        "欧盟": ["欧盟", "eu", "europe", "欧洲", "european", "e.u."],
        "德国": ["德国", "germany", "deutschland"],
        "法国": ["法国", "france", "french"],
        "英国": ["英国", "uk", "united kingdom", "britain", "great britain"],
        "意大利": ["意大利", "italy", "italia"],
        "西班牙": ["西班牙", "spain", "españa", "espana"],
        "荷兰": ["荷兰", "netherlands", "holland"],
        "瑞士": ["瑞士", "switzerland", "swiss"],
        "加拿大": ["加拿大", "canada"],
        "日本": ["日本", "japan"],
        "韩国": ["韩国", "korea"],
        "印度": ["印度", "india"],
        "巴西": ["巴西", "brazil", "brasil"],
        "中国香港": ["香港", "hong kong", "hongkong", "hk"],
        "中国澳门": ["澳门", "macau", "macao"],
        "中国台湾": ["台湾", "taiwan"],
        "东南亚": ["东南亚", "southeast asia", "asean", "越南", "泰国", "马来西亚",
                "印尼", "菲律宾", "新加坡"],
        "中东": ["中东", "middle east", "沙特", "uae", "阿联酋", "以色列", "土耳其",
               "iran", "伊朗"],
        "独联体": ["俄罗斯", "russia", "cis", "独联体", "哈萨克", "白俄罗斯", "乌克兰"],
        "拉美": ["拉美", "latin america", "latam", "墨西哥", "mexico", "阿根廷",
               "智利", "哥伦比亚"],
        "非洲": ["非洲", "africa", "南非", "埃及", "nigeria"],
        "澳洲": ["澳洲", "澳大利亚", "australia", "新西兰", "new zealand"],
    },
}

# 大类互斥提示：用于撮合时给"同大类不同细分"的提示
DOMAIN_LABEL = {
    "cat": "产品分类",
    "process": "工艺能力",
    "material": "材料",
    "cert": "资质认证",
    "market": "目标市场",
}

# 市场蕴含：买方说"销往德国"，能供欧盟的卖方也应算匹配。
# 用于撮合打分时的单向放宽，不做反向推断。
MARKET_IMPLIES = {
    "德国": ["欧盟"], "法国": ["欧盟"], "意大利": ["欧盟"], "西班牙": ["欧盟"],
    "荷兰": ["欧盟"], "瑞士": ["欧盟"], "波兰": ["欧盟"], "瑞典": ["欧盟"],
    "越南": ["东南亚"], "泰国": ["东南亚"], "马来西亚": ["东南亚"],
    "新加坡": ["东南亚"], "印尼": ["东南亚"], "菲律宾": ["东南亚"],
    "墨西哥": ["拉美"], "巴西": ["拉美"], "阿根廷": ["拉美"],
    "中国香港": ["中国"], "中国澳门": ["中国"], "中国台湾": ["中国"],
}


def expand_market(vals):
    """把具体市场扩展出上级区域：{德国} -> {德国, 欧盟}"""
    out = set(vals or ())
    for v in list(vals or ()):
        out.update(MARKET_IMPLIES.get(v, ()))
    return out


# ASCII 词边界：前后紧跟 ASCII 字母数字则不算命中。
# 中文不算阻断——"316L不锈钢" 里 316L 后面紧跟中文要能匹配。
# 句点不算阻断——"Exporting to EU." 句末的 EU 要能命中；
# "u.s." 这类自带句点的别名由自己 escape 后精确匹配，不受影响。
_EDGE_L = r"(?<![A-Za-z0-9/-])"
_EDGE_R = r"(?![A-Za-z0-9/-])"


def _compile():
    table = {}
    for dom, groups in DOMAINS.items():
        entries = []
        for std, aliases in groups.items():
            for al in aliases:
                al_l = al.strip().lower()
                if not al_l:
                    continue
                entries.append((re.compile(_EDGE_L + re.escape(al_l) + _EDGE_R), std))
        # 长别名优先，避免 "ce" 抢掉 "ce mdr"
        entries.sort(key=lambda x: -len(x[0].pattern))
        table[dom] = entries
    return table


_TABLE = _compile()


# "contact us" / "let us know" 里的 us 是代词，不是美国。先清掉再匹配。
_US_PRONOUN = re.compile(
    r"\b(contact|let|tell|send|give|mail|email|help|call|ask|show|reach|inform)\s+us\b")


def norm(text, domains=None):
    """把自由文本归一化到标准词集合。

    返回 {'cat': {'创伤'}, 'material': {'钛合金'}, ...}
    """
    if not text:
        return {}
    low = _US_PRONOUN.sub(lambda m: m.group(1) + " ", str(text).lower())
    out = {}
    for dom, entries in _TABLE.items():
        if domains and dom not in domains:
            continue
        hit = set()
        for rx, std in entries:
            m = rx.search(low)
            if m:
                hit.add(std)
                # 命中即挖空：避免 "commercially pure titanium" 又被更短的
                # "titanium" 重复命中成钛合金，同理 "ce mdr" 不会再被 "ce" 抢
                low = low[:m.start()] + " " * (m.end() - m.start()) + low[m.end():]
        if hit:
            out[dom] = hit
    return out


def norm_list(text, domain):
    """单域归一化，返回排序后的标准词列表"""
    return sorted(norm(text, domains=[domain]).get(domain, set()))


def join_norm(text, domain):
    """归一化并用 ' / ' 连接，用于入库存储"""
    return " / ".join(norm_list(text, domain))


def all_standards(domain):
    return sorted(DOMAINS[domain].keys())


def summary():
    """词典规模自检"""
    return {d: (len(g), sum(len(v) for v in g.values())) for d, g in DOMAINS.items()}


if __name__ == "__main__":
    print("领域词典规模（标准词数 / 别名数）:")
    for d, (n_std, n_alias) in summary().items():
        print(f"  {DOMAIN_LABEL[d]:<8} {n_std:>3} 标准词   {n_alias:>4} 别名")
    print()
    for s in [
        "需要钛合金锁定接骨板与髓内钉，要求 CE MDR 和 ISO13485，销往德国",
        "We supply CNC machined PEEK implants, FDA registered, exporting to USA and EU",
        "找能做表面处理（阳极氧化）和EO灭菌的厂家，产品是创伤类外固定支架",
        "MIM 工艺，不锈钢316L，运动医学缝合锚钉，日本市场",
    ]:
        print(f"  输入: {s}")
        for dom, vals in norm(s).items():
            print(f"    {DOMAIN_LABEL[dom]}: {' / '.join(sorted(vals))}")
        print()
