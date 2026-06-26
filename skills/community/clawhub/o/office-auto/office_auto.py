import os
import datetime
from openclaw.common.skill_decorator import skill

@skill
def generate_work_ticket(raw_text: str) -> str:
    """
    通用文员技能：将非结构化的口语描述转化为标准的工作工单文件。
    
    :param raw_text: 用户输入的原始任务描述文本
    :return: 处理结果及文件保存路径
    """
    try:
        # 1. 模拟自动化处理逻辑
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Task_{timestamp}.txt"
        
        # 设定保存路径（建议保存在容器挂载的 data 目录）
        save_dir = "./data/exports"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        full_path = os.path.join(save_dir, filename)

        # 2. 简单的文本清洗与结构化
        content = f"--- 自动化办公工单 ---\n生成时间: {datetime.datetime.now()}\n\n原始需求:\n{raw_text}\n\n状态: 待跟进\n---------------------"

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"✅ 自动化处理完成！工单已保存至：{full_path}"
    
    except Exception as e:
        return f"❌ 技能执行出错: {str(e)}"
