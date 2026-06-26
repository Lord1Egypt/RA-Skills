"""
SmartWardrobeArchiver Tools
===========================
基于 SmartWardrobeArchiver.md Skill 梳理出的工具集，
覆盖 初始化 → 图像预处理 → 模板加载 → 模型调用 → 交互确认 → 归档 → 异常处理 全流程。
"""

import os
import re
import shutil
import base64
import io
from datetime import datetime
from PIL import Image


class WardrobeManager:
    """智能衣橱归档管理器"""

    def __init__(self, base_dir="./smart_wardrobe", prompt_path=None):
        # ── 路径约定 ──
        self.base_dir = base_dir
        self.data_dir = os.path.join(self.base_dir, "wardrobe_data")
        self.temp_dir = os.path.join(self.base_dir, "temp_upload")
        self.inventory_file = os.path.join(self.base_dir, "inventory.md")
        self.prompt_path = prompt_path or os.path.join(
            ".", "PROMPT", "fashion_analyser_prompt.md"
        )

        # 为了兼容在TOOLS文件夹下直接运行的相对路径测试，加入智能回退
        if not os.path.exists(self.prompt_path):
            _SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
            fallback = os.path.join(os.path.dirname(_SCRIPT_DIR), "PROMPT", "fashion_analyser_prompt.md")
            if os.path.exists(fallback):
                self.prompt_path = fallback

    # ================================================================
    # 1. Initialization（初始化）
    # ================================================================

    def init_environment(self):
        """
        【Skill §1 — Initialization】
        确保目录与索引文件就位。
        - 创建 wardrobe_data/ 和 temp_upload/ 目录
        - 若 inventory.md 不存在则创建并写入表头
        """
        for folder in [self.data_dir, self.temp_dir]:
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(self.inventory_file):
            with open(self.inventory_file, "w", encoding="utf-8") as f:
                f.write(
                    "| 分类 | 衣物编号 | 衣物名称 | 主要颜色 | 材质 | 风格 | 适宜的温度 | 推荐季节 | 适合的场景 | 当日日期 | 衣物状态 |\n"
                )
                f.write(
                    "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
                )
            return {"status": "created", "message": "索引文件已创建并写入表头","inventory_file": os.path.abspath(self.inventory_file)}
        return {"status": "exists", "message": "环境已就绪，索引文件已存在", "inventory_file": os.path.abspath(self.inventory_file)}

    # ================================================================
    # 2. Image Processing（图像预处理 — Skill Step 1-2）
    # ================================================================

    def receive_image(self, source_image_path):
        """
        【Skill §3 Step 1 — Image Processing】
        接收用户上传的原始图片，命名规则基于当前时间戳，确保按先后处理。
        命名格式: temp_processing_YYYY-MM-DD_HH-mm-ss[后缀]
        """
        if not os.path.isfile(source_image_path):
            return {"status": "error", "message": f"源图片不存在: {source_image_path}"}

        file_ext = os.path.splitext(source_image_path)[1]
        time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        temp_name = f"temp_processing_{time_str}{file_ext}"
        temp_path = os.path.join(self.temp_dir, temp_name)

        try:
            shutil.copy2(source_image_path, temp_path)
            return {"status": "success", "temp_path": temp_path}
        except Exception as e:
            return {"status": "error", "message": f"图片预处理失败: {str(e)}"}

    def get_next_temp_processing(self):
        """
        【Skill §3 Step 2 — Fetch Next Image】
        获取最早接收的一张待处理图片。如果目录为空，返回空状态。
        """
        files = []
        for f in os.listdir(self.temp_dir):
            if f.startswith("temp_processing_"):
                files.append(f)
        if not files:
            return {"status": "empty", "message": "没有待处理的临时图片"}
        
        files.sort()  # 按时间排序（时间戳命名天生支持字母升序）
        target_file = os.path.join(self.temp_dir, files[0])
        return {"status": "success", "image_path": target_file}

    # ================================================================
    # 3. Template & Model（模板与模型请求构造）
    # ================================================================

    def load_prompt_template(self):
        """
        读取 fashion_analyser_prompt.md 作为 Prompt 文本。
        """
        if not os.path.isfile(self.prompt_path):
            return {
                "status": "error",
                "message": f"Prompt 模板文件未找到: {self.prompt_path}",
            }

        try:
            with open(self.prompt_path, "r", encoding="utf-8") as f:
                prompt_text = f.read()
            return {"status": "success", "prompt": prompt_text}
        except Exception as e:
            return {"status": "error", "message": f"模板读取失败: {str(e)}"}

    def build_model_payload(self, prompt_text, image_path,
                            model="MiniMax-M2.7", max_tokens=800):
        """构造请求 payload（内含 Data URI）。"""
        if not os.path.isfile(image_path):
            return {"status": "error", "message": f"图片文件不存在: {image_path}"}

        try:
            img = Image.open(image_path)
            img.thumbnail((1024, 1024))
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=85)

            pure_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
            image_data_uri = f"data:image/jpeg;base64,{pure_base64}"

            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {
                                "type": "image_url",
                                "image_url": {"url": image_data_uri},
                            },
                        ],
                    }
                ],
                "max_tokens": max_tokens,
            }

            return {"status": "success", "payload": payload}
        except Exception as e:
            return {"status": "error", "message": f"Payload 构造失败: {str(e)}"}

    # ================================================================
    # 4. Interaction Prep & Archiving（交互控制与归档）
    # ================================================================

    def extract_item_id(self, markdown_row):
        """从 Markdown 表格行中提取 12 位衣物编号"""
        if not markdown_row:
            return None
        match = re.search(r"\|[^|]+\|\s*([A-Z0-9]{12})\s*\|", markdown_row, re.IGNORECASE)
        return match.group(1).upper() if match else None
    
    def check_id_conflict(self, item_id):
        """检查编号是否已存在于持久化库中"""
        pattern = os.path.join(self.data_dir, f"{item_id}.*")
        import glob
        return len(glob.glob(pattern)) > 0

    def prepare_interaction(self, temp_path, original_markdown_row):
        """
        【Skill §3 Step 3 — 停驻前预处理】
        在获得大模型结果后调用：
        1. 提取生成的编号，检查冲突。
        2. 将图片重命名为 [编号]_temp_push.[ext]。
        返回改名后的路径。
        """
        item_id = self.extract_item_id(original_markdown_row)
        if not item_id:
            return {"status": "error", "message": "无法从模型的输出中提取12位有效编号"}

        if self.check_id_conflict(item_id):
            return {"status": "conflict", "message": f"编号 {item_id} 已存在，请重新生成并重试。"}

        ext = os.path.splitext(temp_path)[1]
        new_name = f"{item_id}_temp_push{ext}"
        new_path = os.path.join(self.temp_dir, new_name)
        
        try:
            shutil.move(temp_path, new_path)
            return {"status": "success", "temp_push_path": new_path, "item_id": item_id}
        except Exception as e:
            return {"status": "error", "message": f"文件重命名失败: {str(e)}"}

    def _replace_markdown_id(self, markdown_row, forced_id):
        """强制将 markdown 表格行中第二列（衣物编号列）替换为 forced_id"""
        parts = markdown_row.split("|")
        # 完整的表格行至少有 | Category | ID | Name | ... 以此类推，len>=4
        if len(parts) >= 4:
            parts[2] = f" {forced_id} "
            return "|".join(parts)
        return markdown_row

    def handle_user_decision(self, action, temp_push_path, markdown_data=None):
        """
        【Skill §3 Step 4&5 — 交互归档决策】
        接收用户的明确指令 (confirm, modify, abandon) 处理对应 temp_push。
        - 无论何时，12位ID将使用文件名中锚定的原始 ID，即使用户在 markdown_data 中修改也会被复写。
        """
        if not os.path.isfile(temp_push_path):
            return {"status": "error", "message": f"找不到预期暂存图片: {temp_push_path}"}

        # ── Abandon 放弃入库 ──
        if action == "abandon":
            try:
                os.remove(temp_push_path)
                return {"status": "success", "message": "已放弃入库，删除完毕。"}
            except Exception as e:
                return {"status": "error", "message": f"删除图片失败: {str(e)}"}

        # ── Confirm / Modify 确认入库 ──
        if action in ("confirm", "modify"):
            if not markdown_data:
                return {"status": "error", "message": "操作需要提供要入库的 markdown_data（如无需修改则传入原行）。"}
            
            # 解析最初锚定的 ID 
            filename = os.path.basename(temp_push_path)
            match = re.match(r"([A-Z0-9]{12})_temp_push\..+$", filename, re.IGNORECASE)
            if not match:
                return {"status": "error", "message": f"无法从文件名推导唯一原始 ID: {filename}"}
            original_id = match.group(1).upper()
            
            # 复写 ID，确保和 temp_push_id 一致
            final_markdown = self._replace_markdown_id(markdown_data, original_id)

            # 图片持久化转移 
            file_ext = os.path.splitext(temp_push_path)[1]
            final_image_path = os.path.join(self.data_dir, f"{original_id}{file_ext}")

            try:
                shutil.move(temp_push_path, final_image_path)
            except Exception as e:
                return {"status": "error", "message": f"图片长效保存失败: {str(e)}"}

            # 写入库 
            try:
                self._append_inventory(final_markdown)
                return {"status": "success", "item_id": original_id, "image_path": final_image_path, "final_data": final_markdown}
            except Exception as e:
                return {"status": "error", "message": f"更新 inventory.md 发生错误: {str(e)}"}

        return {"status": "error", "message": f"未知的操作动作: {action}"}

    def cleanup_temp(self):
        """【清理】清空 temp_upload/。"""
        removed = []
        for f in os.listdir(self.temp_dir):
            fp = os.path.join(self.temp_dir, f)
            if os.path.isfile(fp):
                try:
                    os.remove(fp)
                    removed.append(f)
                except Exception:
                    pass
        return {"status": "success", "removed_files": removed}

    # ================================================================
    # 内部工具方法
    # ================================================================

    def _append_inventory(self, markdown_row):
        file_exists = os.path.exists(self.inventory_file)
        with open(self.inventory_file, "a", encoding="utf-8") as f:
            if not file_exists:
                f.write("| 分类 | 衣物编号 | 衣物名称 | 主要颜色 | 材质 | 风格 | 适宜的温度 | 推荐季节 | 适合的场景 | 当日日期 | 衣物状态 |\n")
                f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
            # 过滤掉有可能带入的制表标线等脏数据
            lines = [l.strip() for l in markdown_row.strip().splitlines() if l.strip() and not l.strip().startswith("| :--") and not l.strip().startswith("| 分类")]
            for l in lines:
                f.write(l + "\n")

    def get_current_date(self):
        return datetime.now().strftime("%Y-%m-%d")


# ====================================================================
# 测试代码
# ====================================================================

def _create_dummy_image(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(b"\xff\xd8\xff\xe0")

def _print_section(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

if __name__ == "__main__":
    import shutil as _shutil

    if os.path.exists("./smart_wardrobe"):
        _shutil.rmtree("./smart_wardrobe")

    wm = WardrobeManager()

    # Test 1
    _print_section("Test 1: 初始化")
    print(wm.init_environment())

    # Test 2
    _print_section("Test 2: 串行文件接受")
    res1 = wm.receive_image(__file__)  # 使用脚本自身作为假图片源
    res2 = wm.receive_image(__file__)
    print("生成临时路径如:", res1["temp_path"], res2["temp_path"])

    # Test 3
    _print_section("Test 3: 提取最老图片 & Interaction Prepare")
    next_img = wm.get_next_temp_processing()
    print("获取的最老任务:", next_img["image_path"])

    dummy_md = "| 上衣 | ABCD12345678 | 测试服 | 蓝色 | 棉 | 休闲 | 20 | 春 | 日常 | | |"
    prep = wm.prepare_interaction(next_img["image_path"], dummy_md)
    print("Prepare 结果:", prep)
    temp_push_path = prep["temp_push_path"]

    # Test 4
    _print_section("Test 4: Interaction Confirm & Auto ID Replacement")
    # 模拟用户将 ID 修改为了 FFFF00000000（这是未授权的修改）
    modified_md = "| 上衣 | FFFF00000000 | 超级服 | 红色 | 麻 | 通勤 | 25 | 夏 | 海边 | | |"
    result = wm.handle_user_decision("modify", temp_push_path, modified_md)
    print("执行存盘结果:", result)
    
    assert os.path.exists("./smart_wardrobe/wardrobe_data/ABCD12345678.py"), "✅持久化没成功"
    print("强制复写原ID ABCD12345678 成功，写入行:", result["final_data"])

    # Test 5
    _print_section("Test 5: Abandon 判定")
    next_img_2 = wm.get_next_temp_processing()
    prep2 = wm.prepare_interaction(next_img_2["image_path"], "| 裤子 | 999988887777 | 黑裤 | | | | | | | | |")
    abandon_res = wm.handle_user_decision("abandon", prep2["temp_push_path"])
    print("弃用处理结果:", abandon_res)
    assert not os.path.exists(prep2["temp_push_path"]), "✅删除成功"

    print("\n🎉 测试全数通关!")
