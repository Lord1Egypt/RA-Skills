"""
knowledge-collector 核心收集逻辑
支持3种入口：群聊自动识别/主动记录/批量导入
自动分类（4方向×4层级）+ 信息提取 + 模板填充 + domain-kit入库
"""
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# 添加 domain-kit 路径
DOMAIN_KIT_PATH = Path(__file__).parent.parent.parent / "domain-kit"
sys.path.insert(0, str(DOMAIN_KIT_PATH))

from storage.knowledge_store import KnowledgeStore
from utils.id_generator import generate_entity_id

# 加载关键词词典
KEYWORDS_PATH = Path(__file__).parent.parent / "config" / "keywords.json"
with open(KEYWORDS_PATH, "r", encoding="utf-8") as f:
    KEYWORDS = json.load(f)

# 模板路径
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

# domain-kit 存储路径
STORAGE_PATH = DOMAIN_KIT_PATH / "storage"


def classify(text: str) -> dict:
    """
    根据关键词自动分类
    返回: {"direction": str, "type": str, "level": str, "confidence": float}
    """
    text_lower = text.lower()
    
    # 方向分类
    direction_scores = {}
    for direction, keywords in KEYWORDS["directions"].items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        direction_scores[direction] = score
    
    # 类型分类
    type_scores = {}
    for typ, keywords in KEYWORDS["types"].items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        type_scores[typ] = score
    
    # 层级分类
    level_scores = {}
    for level, keywords in KEYWORDS["levels"].items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        level_scores[level] = score
    
    # 取最高分
    direction = max(direction_scores, key=direction_scores.get) if any(direction_scores.values()) else "非标自动化"
    typ = max(type_scores, key=type_scores.get) if any(type_scores.values()) else "经验"
    level = max(level_scores, key=level_scores.get) if any(level_scores.values()) else "L4"
    
    # 计算置信度
    max_dir_score = max(direction_scores.values()) if direction_scores else 0
    max_type_score = max(type_scores.values()) if type_scores else 0
    max_level_score = max(level_scores.values()) if level_scores else 0
    total_keywords = max_dir_score + max_type_score + max_level_score
    confidence = min(0.95, 0.5 + total_keywords * 0.1)
    
    return {
        "direction": direction,
        "type": typ,
        "level": level,
        "confidence": confidence
    }


def extract_metadata(text: str) -> dict:
    """
    提取结构化字段：设备型号、项目编号、协议名称等
    """
    metadata = {
        "equipment_models": [],
        "protocols": [],
        "project_ids": [],
        "tags": []
    }
    
    # 提取设备型号
    for model in KEYWORDS["equipment_models"]:
        if model.lower() in text.lower():
            metadata["equipment_models"].append(model)
            metadata["tags"].append(model)
    
    # 提取协议名称
    for protocol in KEYWORDS["protocols"]:
        if protocol.lower() in text.lower():
            metadata["protocols"].append(protocol)
            metadata["tags"].append(protocol)
    
    # 提取项目编号
    project_pattern = KEYWORDS["project_pattern"]
    matches = re.findall(project_pattern, text, re.IGNORECASE)
    metadata["project_ids"] = list(set(matches))
    metadata["tags"].extend(metadata["project_ids"])
    
    # 去重
    metadata["tags"] = list(set(metadata["tags"]))
    
    return metadata


def fill_template(classification: dict, metadata: dict, raw_text: str, title: str = None) -> str:
    """
    根据分类填充对应模板
    """
    typ = classification["type"]
    
    # 选择模板文件
    template_map = {
        "方案": "solution.md",
        "设计": "design.md",
        "软件": "software.md",
        "算法": "algorithm.md",
        "经验": "experience.md"
    }
    template_file = TEMPLATES_DIR / template_map.get(typ, "experience.md")
    
    # 读取模板
    with open(template_file, "r", encoding="utf-8") as f:
        template_content = f.read()
    
    # 填充标题
    if not title:
        # 从文本第一行提取标题
        first_line = raw_text.strip().split("\n")[0]
        title = first_line[:50] if len(first_line) > 50 else first_line
    
    # 填充元数据
    now = datetime.now().strftime("%Y-%m-%d")
    tags_str = ", ".join(metadata.get("tags", []))
    
    # 替换模板变量（支持 {{var}} 和 [var] 两种格式）
    content = template_content
    content = content.replace("{{title}}", title).replace("[标题]", title)
    content = content.replace("{{date}}", now).replace("[YYYY-MM-DD]", now)
    content = content.replace("{{tags}}", tags_str).replace("[关键词]", tags_str)
    
    # 填充其他变量
    content = content.replace("{{experience_type}}", classification.get("type", "经验"))
    content = content.replace("{{project_id}}", ", ".join(metadata.get("project_ids", [])))
    content = content.replace("{{confidence}}", str(classification.get("confidence", 0.8)))
    content = content.replace("{{contributor}}", "待填写")
    
    # 添加原始内容
    content += f"\n\n## 原始内容\n\n{raw_text}\n"
    
    return content


def save_to_domain_kit(markdown_content: str, classification: dict, metadata: dict) -> str:
    """
    写入 domain-kit 知识库
    返回 entity_id
    """
    store = KnowledgeStore(str(STORAGE_PATH))
    
    # 实体类型映射
    type_mapping = {
        "方案": "BestPractice",  # 暂用 BestPractice
        "设计": "BestPractice",
        "软件": "CodeTemplate",
        "算法": "BestPractice",
        "经验": "BestPractice"
    }
    entity_type = type_mapping.get(classification["type"], "BestPractice")
    
    # 构建实体数据
    entity_data = {
        "title": markdown_content.split("\n")[0].replace("# ", ""),
        "direction": classification["direction"],
        "type": classification["type"],
        "level": classification["level"],
        "content": markdown_content,
        "equipment_models": metadata.get("equipment_models", []),
        "protocols": metadata.get("protocols", []),
        "project_ids": metadata.get("project_ids", [])
    }
    
    # 生成幂等 ID
    entity_id = generate_entity_id(entity_type, entity_data, "knowledge-collector")
    
    # 写入存储
    tags = metadata.get("tags", []) + [classification["direction"], classification["type"], classification["level"]]
    store.add_entity(
        entity_id,
        entity_type,
        entity_data,
        provenance={
            "source_type": "manual",
            "source_path": "knowledge-collector",
            "extracted_at": datetime.now().isoformat(),
            "confidence": classification["confidence"]
        },
        tags=tags
    )
    
    return entity_id


def notify_reviewer(research_room: str, entity_id: str, title: str):
    """
    推送给研究室负责人（预留接口）
    """
    reviewers_path = Path(__file__).parent.parent / "config" / "reviewers.json"
    with open(reviewers_path, "r", encoding="utf-8") as f:
        reviewers = json.load(f)
    
    reviewer_info = reviewers.get(research_room, {})
    reviewer_name = reviewer_info.get("reviewer", "待配置")
    mx_id = reviewer_info.get("mx_id", "")
    
    # 生成待办消息
    message = f"""📋 新知识待审核

标题: {title}
ID: {entity_id}
研究室: {research_room}

请审核该知识条目。
"""
    
    # 预留美信发送接口
    print(f"[通知] 发送给 {reviewer_name} ({mx_id}):")
    print(message)
    
    return {"reviewer": reviewer_name, "mx_id": mx_id, "message": message}


def collect(input_text: str, source_type: str = "manual", title: str = None) -> dict:
    """
    主流程：收集 → 分类 → 提取 → 填充 → 入库 → 通知
    """
    # 1. 自动分类
    classification = classify(input_text)
    
    # 2. 提取元数据
    metadata = extract_metadata(input_text)
    
    # 3. 填充模板
    markdown_content = fill_template(classification, metadata, input_text, title)
    
    # 4. 写入 domain-kit
    entity_id = save_to_domain_kit(markdown_content, classification, metadata)
    
    # 5. 确定研究室并通知
    direction_to_room = {
        "非标自动化": "机电系统研究室",
        "物流自动化": "物流自动化研究室",
        "工业视觉": "工业视觉研究室"
    }
    research_room = direction_to_room.get(classification["direction"], "机电系统研究室")
    
    title_text = title or markdown_content.split("\n")[0].replace("# ", "")
    notify_result = notify_reviewer(research_room, entity_id, title_text)
    
    return {
        "entity_id": entity_id,
        "classification": classification,
        "metadata": metadata,
        "research_room": research_room,
        "notify_result": notify_result,
        "markdown_path": None  # 可选：保存为 Markdown 文件
    }


if __name__ == "__main__":
    # 演示
    demo_text = """
    AM600 EtherCAT 从站掉线排查经验
    
    项目 IV2615 调试过程中，发现 AM600 PLC 的 EtherCAT 从站频繁掉线。
    
    问题现象：运行2小时后，伺服驱动器 IS620N 从站掉线，报警代码 0x3021。
    
    根因分析：EtherCAT 网线屏蔽层未接地，导致电磁干扰。
    
    解决方案：
    1. 更换屏蔽网线
    2. 屏蔽层单端接地
    3. 增加磁环
    
    预防措施：所有 EtherCAT 网线必须使用屏蔽线，且屏蔽层单端接地。
    """
    
    result = collect(demo_text, source_type="manual", title="AM600 EtherCAT 从站掉线排查")
    print("\n收集结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
