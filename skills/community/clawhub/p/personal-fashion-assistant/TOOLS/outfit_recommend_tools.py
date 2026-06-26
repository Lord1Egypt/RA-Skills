# -*- coding: utf-8 -*-
"""
SmartWardrobeArchiver Tools - Outfit Recommendation
===========================
用于处理每日穿搭推荐的核心工具：读取并过滤库存，替换提示词模板，构造大模型请求 payload。
"""

import os

class OutfitRecommendManager:
    """每日穿搭推荐管理器"""

    def __init__(self, base_dir="./smart_wardrobe", prompt_path=None):
        self.base_dir = base_dir
        self.inventory_file = os.path.join(self.base_dir, "inventory.md")
        self.prompt_path = prompt_path or os.path.join(
            ".", "PROMPT", "outfit_recommend_prompt.md"
        )
        
        # 兼容相对路径
        if not os.path.exists(self.prompt_path):
            _SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
            fallback = os.path.join(os.path.dirname(_SCRIPT_DIR), "PROMPT", "outfit_recommend_prompt.md")
            if os.path.exists(fallback):
                self.prompt_path = fallback

    def get_filtered_inventory(self, washing_ids=None):
        """
        读取 inventory.md，过滤掉处于洗涤中或不可用状态的衣物。
        washing_ids: list of str, 包含洗涤中衣物的编号。
        返回过滤后的 Markdown 表格文本。
        """
        if not os.path.exists(self.inventory_file):
            return "衣橱暂无数据。"
        
        washing_ids = washing_ids or []
        filtered_lines = []
        
        try:
            with open(self.inventory_file, "r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    # 保留非表格内容或表头
                    if not stripped.startswith("|") or stripped.startswith("| :--") or stripped.startswith("| 分类"):
                        filtered_lines.append(stripped)
                        continue
                    
                    # 检查此行是否包含洗涤中的ID
                    is_washing = False
                    for w_id in washing_ids:
                        if w_id and w_id in stripped:
                            is_washing = True
                            break
                    
                    if not is_washing:
                        filtered_lines.append(stripped)
                        
            return "\n".join(filtered_lines)
        except Exception as e:
            return f"读取库存文件失败: {str(e)}"

    def build_recommend_prompt(self, user_style, location, min_temp, max_temp, weather, scene, washing_ids=None):
        """
        构建填入上下文数据的穿搭推荐提示词。
        """
        # 1. 检查模板文件是否存在
        if not os.path.exists(self.prompt_path):
            return {"status": "error", "message": f"提示词模板不存在: {self.prompt_path}"}
            
        # 2. 读取模板
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            template = f.read()
            
        # 3. 获取过滤后的库存数据
        inventory_data = self.get_filtered_inventory(washing_ids)
        
        # 4. 替换占位符
        template = template.replace("{{用户风格关键词}}", str(user_style))
        template = template.replace("{{用户当前位置}}", str(location))
        template = template.replace("{{最低温}}", str(min_temp))
        template = template.replace("{{最高温}}", str(max_temp))
        template = template.replace("{{阴晴/风力}}", str(weather))
        template = template.replace("{{日常通勤}}", str(scene))
        template = template.replace("{{此处粘贴 inventory.md 中的数据，需包含编号、适宜温度、风格等字段}}", inventory_data)
        
        return {"status": "success", "prompt": template}

    def build_model_payload(self, prompt_text, model="MiniMax-M2.7", max_tokens=1500):
        """
        构造 MiniMax 模型的请求 payload。此处仅为文本推荐不需要传入图片。
        """
        try:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt_text
                    }
                ],
                "max_tokens": max_tokens,
            }
            return {"status": "success", "payload": payload}
        except Exception as e:
            return {"status": "error", "message": f"Payload 构造失败: {str(e)}"}

if __name__ == "__main__":
    # 简单的本地单元测试
    manager = OutfitRecommendManager(base_dir=".")
    
    res = manager.build_recommend_prompt(
        user_style="法式优雅、极简",
        location="北京市朝阳区",
        min_temp="10",
        max_temp="22",
        weather="晴，微风",
        scene="职场商务会议",
        washing_ids=["TEST12345678"]
    )
    
    if res["status"] == "success":
        print("✅ 提示词生成成功：\n")
        print(res["prompt"][:500] + "\n...\n")
        
        payload_res = manager.build_model_payload(res["prompt"])
        print(f"Payload 状态: {payload_res['status']}")
    else:
        print(f"❌ 错误: {res['message']}")
