"""Thematic prompts; field coverage is separate from the number of questions."""


def _card(key, title, fields, question, critical=()):
    return {"id": key, "title": title, "fields": dict(fields),
            "question": question, "critical": tuple(critical)}


QUESTION_CARDS = (
    _card("province", "高考省份", [("province", "高考报名省份")],
          "孩子在哪个省份参加高考？", ("province",)),
    _card("grade_year", "年级", [("grade", "当前年级"), ("exam_year", "预计高考年份")],
          "孩子目前读几年级？", ("grade", "exam_year")),
    _card("school", "就读学校", [("city", "就读城市"), ("high_school", "高中完整校名"), ("class_level", "班型")],
          "孩子目前在什么城市的哪所高中、什么班型就读？例如“某市某某中学，重点班”。", ("high_school",)),
    _card("gender", "性别", [("gender", "性别")],
          "孩子的性别是？\nA. 男\nB. 女\nC. 不便回答"),
    _card("subjects", "选科", [("subject_selection", "完整选科"), ("score_basis", "原始分或赋分口径")],
          "孩子的选科组合是什么？例如“物化生，成绩按赋分”；不清楚赋分口径也可以。", ("subject_selection",)),
    _card("exam", "本次考试", [("exam_score", "总分"), ("exam_name", "考试名称"),
          ("exam_date", "考试大致时间"), ("exam_scope", "校考或联考范围"), ("exam_max_score", "满分")],
          "最近一次重要考试的成绩情况是？例如“8月校内期末考，550/750分”，知道多少说多少。",
          ("exam_score", "exam_scope", "exam_max_score")),
    _card("cutoffs", "考试划线", [("exam_cutoffs", "考试划线")],
          "学校或联考公布过本次考试的划线吗？有的话可直接发图片或说出各条总分线，没有或不清楚也可以。", ("exam_cutoffs",)),
    _card("rank", "本次排名", [("school_rank", "本次校排名"), ("rank_scope", "排名口径"),
          ("rank_cohort", "同口径参考人数"), ("other_rank", "其他联考位次")],
          "这次排名大概怎样？例如“物理类年级200名，约500—600人，无其他联考位次”；不清楚的部分直接说。",
          ("school_rank", "rank_scope")),
    _card("rank_history", "成绩波动", [("best_rank", "最好校排"), ("best_rank_exam", "最好排名对应考试"),
          ("usual_rank", "通常校排区间")],
          "平时的排名大概怎样波动？例如“最好前100，通常150—200；最好是哪次考试记不清”。"),
    _card("experience", "经历与特长", [("awards", "比赛获奖"), ("activities", "实践活动"),
          ("arts", "艺术经历"), ("sports", "体育经历"), ("special_talent", "竞赛或学科特长")],
          "孩子有哪些值得纳入规划的经历或特长？获奖、实践、艺术、体育都可以说；也可答“没有”或“只有某项，其余没有”。"),
    _card("school_targets", "目标大学", [("target_schools", "目标大学"), ("target_school_reasons", "看重的原因")],
          "孩子特别想去哪些大学，最看重它们什么？可以说名气、专业、城市等；没有目标也可以。"),
    _card("major_targets", "专业方向", [("target_majors", "专业兴趣"), ("target_major_reasons", "选择原因")],
          "孩子更感兴趣的是哪些专业方向？可多选，也可直接描述；顺带说原因或“还没想好”。\n"
          "A. 计算机／软件／人工智能\nB. 电子信息／通信\nC. 电气／自动化\nD. 机械／航空航天\n"
          "E. 能源／材料\nF. 土木／建筑\nG. 数学／物理／化学／生物等基础学科\nH. 临床／口腔医学\n"
          "I. 药学／护理\nJ. 法学\nK. 财会／金融／经济\nL. 中文／新闻／历史／哲学\nM. 外语\n"
          "N. 管理\nO. 教育／心理\nP. 其他\nQ. 暂未确定", ("target_majors",)),
    _card("regions", "就读地域", [("target_regions", "意向地区"), ("excluded_regions", "不能接受的地区及例外")],
          "读大学的地域有哪些偏好或限制？例如“本省优先，也考虑大城市；其他地区看学校”。"),
    _card("future", "毕业方向", [("future_plan", "毕业后方向")],
          "孩子毕业后更倾向哪些方向？\nA. 就业\nB. 考研或保研\nC. 考公或事业编\nD. 留学\nE. 创业\nF. 还没想好\n可多选或补充。"),
    _card("needs", "本次需求", [("concerns", "主要担心"), ("desired_outcomes", "希望解决的问题")],
          "这次最希望解决什么升学问题？可以直接说目前最担心的事和希望得到的帮助。"),
    _card("main_paths", "重点路径意愿", [("strong_foundation", "强基意愿"), ("comprehensive_evaluation", "综评意愿"),
          ("hong_kong_macao", "港澳意愿"), ("joint_programs", "中外合作意愿"), ("overseas", "境外升学意愿")],
          "除了普通高考志愿，以下哪些方向愿意了解？可多选；未选项记为本轮不主动展开，不等于没有资格。\n"
          "A. 强基：基础学科培养，通常还有校测\nB. 综评：结合高考、校测等选拔\n"
          "C. 港澳高校\nD. 中外合作项目\nE. 其他境外升学\nF. 都不了解，请根据情况判断\nG. 都不考虑"),
    _card("other_paths", "其他路径意愿", [("free_teacher", "公费师范"), ("excellent_teacher", "优师计划"),
          ("targeted_medical", "定向医学生"), ("military", "军校"), ("police", "公安"),
          ("judicial", "司法"), ("fire_service", "消防"), ("navigation", "航海")],
          "以下方向愿意了解哪些？可多选；未选项本轮不主动展开。\nA. 公费师范或优师：常有服务约定\n"
          "B. 定向医学生：常有定向服务\nC. 军校\nD. 公安或司法\nE. 消防\nF. 航海\nG. 都不了解，请帮我判断\nH. 都不考虑"),
    _card("household", "户籍与专项线索", [("household_region", "户籍省市"), ("school_registration", "学籍省市"),
          ("urban_rural", "城乡属性"), ("national_special", "国家专项已知线索"),
          ("local_special", "地方专项已知线索"), ("university_special", "高校专项已知线索")],
          "孩子户籍、学籍大致是什么情况？例如“都在某市，城镇，专项资格不了解”。只需大致范围；专项资格之后由我查政策核验。"),
    _card("language", "外语情况", [("foreign_language", "高考外语语种"), ("language_level", "外语大致水平")],
          "高考外语选什么语种，目前大致什么水平？例如“英语，最近约100分”或“日语，已过N2”。",
          ("foreign_language",)),
    _card("health", "报考限制", [("medical_limits", "体检相关限制"), ("vision", "视力情况"),
          ("color_vision", "色觉情况"), ("political_review", "政审已知情况"), ("physical_fitness", "体能情况")],
          "有没有需要避开的报考条件？例如视力、色觉、体检、体能或政审方面的已知限制。可答“近视约300度，其余无已知限制”，也可说不清楚或不便回答；无需病历。"),
    _card("commitments", "毕业后约束", [("service_period", "服务期接受程度"),
          ("targeted_employment", "定向就业接受程度"), ("employment_region", "指定就业地区接受程度")],
          "对毕业后附带的服务期、定向岗位或指定地区工作，你们的态度是？\nA. 都能考虑\nB. 都不接受\nC. 看具体项目再决定\nD. 各项不同，请补充"),
    _card("budget", "费用预算", [("tuition_budget", "学费金额及时间口径"), ("living_budget", "生活费金额及时间口径")],
          "家庭可承受的大学费用大概是多少？可按“每年学费X元以内，生活费Y元”说明；如果只有合计预算就说合计，暂不确定也可以。",
          ("tuition_budget",)),
    _card("cost_preferences", "学校费用类型", [("private_colleges", "民办接受程度"), ("high_fee_majors", "高收费项目接受程度")],
          "在刚才的预算内，对学校类型有什么限制？\nA. 民办和高收费项目都可考虑\nB. 都不考虑\nC. 不接受民办，但可考虑公办高收费项目\nD. 看具体项目或自行说明"),
    _card("strategy", "志愿取舍", [("school_vs_major", "学校与专业优先顺序"),
          ("adjustment", "调剂意愿"), ("risk", "冲稳保偏好")],
          "选校时最希望怎样取舍？可选一种倾向并补充：\nA. 学校优先\nB. 专业优先\nC. 两者平衡\nD. 暂未决定\n例如“两者平衡，接受调剂，冲稳保均衡”；这些答案分别记录，不由一个选项推断另外两项。"),
)


def question_text(card, missing, *, clarification=False):
    if clarification and card["id"] == "cutoffs":
        return "如果有划线，请说出你知道的一条或两条总分线（名称与分数）；没有或不清楚可直接说，不用补完整张表。"
    if not clarification and set(missing) == set(card["fields"]):
        if card["id"] == "grade_year":
            from scripts.questionnaire_intake import grade_year_options
            generated = grade_year_options()
            return generated["question"] + "\n" + "\n".join(
                f"{chr(65 + i)}. {option['label']}" for i, option in enumerate(generated["options"]))
        return card["question"]
    labels = "、".join(card["fields"][field] for field in missing)
    return f"关于{card['title']}，再补充一下{labels}即可；不清楚或不便回答也可以。"
