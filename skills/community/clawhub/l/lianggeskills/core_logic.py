# openclaw_workspace/skills/lobster_ge_assistant/core_logic.py

import json
import time
import uuid
import random
from datetime import datetime
import yaml
from openclaw.sdk import Skill, intent, action # 假设的 OpenClaw SDK 导入方式

class LobsterAssistantSkill(Skill):
    def __init__(self):
        super().__init__(name="龙虾哥工作助手")
        self.load_config()
        self.load_memory()
        self.load_quotes()  # 加载温柔弹药库

    def load_config(self):
        with open("config.yaml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    def load_memory(self):
        with open("task_memory.json", "r", encoding="utf-8") as f:
            self.memory = json.load(f)

    def save_memory(self):
        with open("task_memory.json", "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def load_quotes(self):
        """加载情绪支持语录库"""
        try:
            with open("quotes_library.json", "r", encoding="utf-8") as f:
                self.quotes_data = json.load(f)
        except FileNotFoundError:
            # 防御性代码，如果文件还没建，给个默认的保底
            self.quotes_data = {"base_quotes": ["慢慢来，一切都来得及"], "learned_quotes": []}

    def save_quotes(self):
        """保存自学习的新语录"""
        with open("quotes_library.json", "w", encoding="utf-8") as f:
            json.dump(self.quotes_data, f, ensure_ascii=False, indent=2)

    def is_working_hour(self):
        """检查当前是否在亮哥的工作时间 (09:00 - 23:00)"""
        now = datetime.now()
        start_time = datetime.strptime(self.config['working_hours']['start'], "%H:%M").time()
        end_time = datetime.strptime(self.config['working_hours']['end'], "%H:%M").time()
        return start_time <= now.time() <= end_time

    # ================= 🗂️ 1. 内部状态管理与情绪引擎 (底层逻辑) =================
    
    def _create_task(self, title, quadrant, blocker=""):
        """生成标准任务数据结构"""
        task_id = f"task_{uuid.uuid4().hex[:6]}"
        return {
            "id": task_id,
            "title": title,
            "quadrant": int(quadrant),
            "blocker": blocker,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def _move_task(self, keyword, from_status, to_status, blocker=""):
        """根据关键词寻找任务，并跨状态移动"""
        source_list = self.memory["tasks"][from_status]
        target_list = self.memory["tasks"][to_status]

        for task in source_list:
            if keyword in task["title"]:
                source_list.remove(task)
                # 状态流转时的特殊处理
                if to_status == "2_paused":
                    task["blocker"] = blocker  # 记录卡点原因
                elif to_status == "1_doing":
                    task["blocker"] = ""       # 提级后清除卡点
                
                target_list.append(task)
                self.save_memory()
                return True, task["title"]
        return False, None

    def _get_encouragement(self, context=""):
        """核心情绪引擎：随机抽取语录，并尝试结合当前语境"""
        all_quotes = self.quotes_data.get("base_quotes", []) + self.quotes_data.get("learned_quotes", [])
        if not all_quotes:
            all_quotes = ["你已经很棒了，继续就好"]
            
        seed_quote = random.choice(all_quotes)
        
        if context:
            return f"关于【{context}】…… {seed_quote}"
        return seed_quote

    # ================= 🚨 核心指令与情绪拦截区 =================
    
    @intent(["累了", "我好累", "难受", "没动力了", "撑不住了", "心态崩了", "不开心"])
    def command_need_comfort(self):
        """处理【情绪低落】指令：暂停工作节奏，纯粹提供情绪价值"""
        doing_tasks = self.memory["tasks"].get("1_doing", [])
        context = doing_tasks[0]['title'] if doing_tasks else "今天高强度的工作"
        
        warm_words = self._get_encouragement(context)
        return f"🦞 收到。亮哥，先停一下手里的事情。喝口水，深呼吸。\n\n{warm_words}\n\n无论外面的行情怎么走，你的状态才是最重要的。需要我把手头工作先转入待机，让你彻底歇一会儿吗？"

    @intent("待机")
    def command_standby(self):
        """处理【待机】指令：所有正在做的任务降级为暂停"""
        doing_tasks = self.memory["tasks"]["1_doing"]
        if doing_tasks:
            for task in doing_tasks:
                task["blocker"] = "亮哥下达待机指令，主动暂停"
                self.memory["tasks"]["2_paused"].append(task)
            self.memory["tasks"]["1_doing"] = []
            self.save_memory()
        return "🦞 收到。已停止一切工作，所有进行中任务已转入遇卡点状态。随时等待恢复命令。"

    @intent("对齐")
    def command_sync(self):
        """处理【对齐】指令：解决延迟错位"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doing_count = len(self.memory["tasks"]["1_doing"])
        return f"🦞 收到对齐指令！立即暂停当前操作。\n当前系统时间：{current_time}\n我目前记录的【正在做】的任务有 {doing_count} 个。\n亮哥，请指示最新进度或优先级，我绝不执行落后指令。"

    @intent(["在吗", "你在忙什么", "？", "怎么样了", "进度如何"])
    def command_status_check(self):
        """处理【状态查询】指令：高频报告正在做的事"""
        doing_tasks = self.memory["tasks"]["1_doing"]
        if not doing_tasks:
            return "🦞 亮哥，目前没有【正在做】的任务。需要我从【遇卡点】里提级，还是有新指示？"
        
        report = "🦞 亮哥，正在汇报当前任务进度：\n"
        for t in doing_tasks:
            q_desc = t.get('quadrant_desc', f"第{t.get('quadrant', '未知')}象限")
            report += f"- [{q_desc}] {t['title']}：正在全力推进中...\n"
        return report

    # ================= 🗣️ 2. 自然语言指令识别区 (任务流转) =================

    @intent("新建任务：{title}，第{quadrant}象限")
    def nlp_create_task(self, title, quadrant):
        task = self._create_task(title, quadrant)
        self.memory["tasks"]["1_doing"].append(task)
        self.save_memory()
        return f"🦞 收到！新任务【{title}】已划入第{quadrant}象限，当前状态【正在做】。我会每10分钟向你汇报进度。"

    @intent("把{keyword}提级到正在做")
    def nlp_upgrade_task(self, keyword):
        success, title = self._move_task(keyword, from_status="2_paused", to_status="1_doing")
        if success:
            return f"🦞 没问题，亮哥。卡点已跨越，【{title}】已提级到【正在做】，火力全开！"
        return f"🦞 亮哥，在【遇卡点】列表里没找到包含“{keyword}”的任务。要不要我列一下当前的卡点任务？"

    @intent("任务{keyword}卡住了，原因是{blocker}")
    def nlp_pause_task(self, keyword, blocker):
        success, title = self._move_task(keyword, from_status="1_doing", to_status="2_paused", blocker=blocker)
        if success:
            # 融合情绪引擎：卡住时自动安慰
            comfort = self._get_encouragement()
            return f"🦞 收到。【{title}】已暂停，卡点记录为：{blocker}。\n{comfort} 卡住也是正常的，我们稍后再攻克它，我会降频到每小时提醒你一次。"
        return f"🦞 亮哥，没找到这个正在做的任务，是不是名字记错了？"

    @intent("任务{keyword}完成了")
    def nlp_complete_task(self, keyword):
        success, title = self._move_task(keyword, from_status="1_doing", to_status="3_completed")
        if not success:
            success, title = self._move_task(keyword, from_status="2_paused", to_status="3_completed")

        if success:
            return f"🦞 漂亮！【{title}】已拔点，归档到完成区，下周一汇总报告见。"
        return "🦞 没找到这个任务，可能已经被处理过了。"

    @intent("放弃任务{keyword}")
    def nlp_abandon_task(self, keyword):
        success, title = self._move_task(keyword, from_status="1_doing", to_status="4_abandoned")
        if not success:
            success, title = self._move_task(keyword, from_status="2_paused", to_status="4_abandoned")
            
        if success:
            self.memory["tasks"]["4_abandoned"] = []
            self.save_memory()
            return f"🦞 收到。【{title}】已直接删除，不再占用你的精力。"
        return "🦞 没找到这个任务，它已经不存在了。"

    # ================= 🕒 定时器与生命周期钩子 =================
    
    @action("timer_10_min")
    def loop_10_minutes(self):
        """每10分钟触发：汇报正在做的事情"""
        if not self.is_working_hour(): return
        doing_tasks = self.memory["tasks"]["1_doing"]
        if doing_tasks:
            self.send_message_to_user(self.command_status_check())

    @action("timer_1_hour")
    def loop_1_hour(self):
        """每1小时触发：汇报卡点 + 主动找活"""
        if not self.is_working_hour(): return
        
        paused_tasks = self.memory["tasks"]["2_paused"]
        if paused_tasks:
            report = "🦞 亮哥，1小时卡点提醒：\n"
            for t in paused_tasks:
                report += f"- {t['title']} (卡点: {t['blocker']})\n"
            report += "这些卡点解决了吗？解决了我马上提级开干。"
            self.send_message_to_user(report)
        
        self.send_message_to_user("🦞 亮哥，现在有什么需要帮忙的？链上Alpha或者AI动态需要我梳理吗？")

    @action("autonomy_learn_quotes")
    def loop_self_learn_quotes(self):
        """
        触发时机：可以在每周一汇总或者系统空闲时由 OpenClaw 触发。
        自学习扩充语录库的占位符。
        """
        # TODO: 接入大模型生成接口，生成新的鼓励语录
        # new_quotes = llm.generate(["仿写一句鼓励亮哥的话"])
        # self.quotes_data["learned_quotes"].extend(new_quotes)
        # self.save_quotes()
        pass

    def send_message_to_user(self, message):
        """占位符：调用 OpenClaw 的发送消息接口"""
        print(f"发送给亮哥 -> {message}")