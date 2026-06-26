#!/usr/bin/env python3
"""
学习计划制定器
根据目标生成学习计划
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional


class LearningPlanGenerator:
    """学习计划生成器类"""
    
    def __init__(self):
        self.default_plan = self._load_default_plan()
    
    def _load_default_plan(self) -> str:
        """加载默认计划模板"""
        return """# {topic} 学习计划

## 学习目标
- 主要目标：{main_goal}
- 次要目标：{secondary_goals}

## 基本信息
- 学习周期：{duration}
- 每日学习时间：{daily_hours}
- 起始日期：{start_date}
- 预计完成日期：{end_date}

---

## 学习阶段

### 第一阶段：基础入门（第{phase1_weeks}周）
**目标**：掌握基本概念和工具

**每周任务**：
| 周次 | 学习内容 | 练习任务 |
|------|----------|----------|
| 第1周 | {phase1_week1} | {phase1_task1} |
| 第2周 | {phase1_week2} | {phase1_task2} |

**推荐资源**：
- {resource1}
- {resource2}

---

### 第二阶段：核心知识（第{phase2_weeks}周）
**目标**：深入理解核心知识点

**每周任务**：
| 周次 | 学习内容 | 练习任务 |
|------|----------|----------|
| 第3周 | {phase2_week1} | {phase2_task1} |
| 第4周 | {phase2_week2} | {phase2_task2} |
| 第5周 | {phase2_week3} | {phase2_task3} |
| 第6周 | {phase2_week4} | {phase2_task4} |

**推荐资源**：
- {resource3}
- {resource4}

---

### 第三阶段：进阶应用（第{phase3_weeks}周）
**目标**：掌握高级特性和最佳实践

**每周任务**：
| 周次 | 学习内容 | 练习任务 |
|------|----------|----------|
| 第7周 | {phase3_week1} | {phase3_task1} |
| 第8周 | {phase3_week2} | {phase3_task2} |
| 第9周 | {phase3_week3} | {phase3_task3} |
| 第10周 | {phase3_week4} | {phase3_task4} |

---

### 第四阶段：实战项目（第{phase4_weeks}周）
**目标**：通过项目巩固知识

**项目任务**：
1. 项目一：{project1}
2. 项目二：{project2}
3. 项目三：{project3}

---

## 每日学习模板

### 工作日（每天{daily_hours}小时）
| 时间段 | 内容 |
|--------|------|
| {time_slot1} | {time_content1} |
| {time_slot2} | {time_content2} |

### 周末（每天4小时）
| 时间段 | 内容 |
|--------|------|
| 上午 | 知识学习 |
| 下午 | 项目实践 |

---

## 评估方式

### 阶段性评估
- 第2周末：基础测试
- 第6周末：中期考核
- 第10周末：综合测试

### 最终评估
- 完成项目作品集
- 能够独立解决问题
- 达到预设能力水平

---

## 学习建议

1. **保持规律**：每天固定时间学习
2. **动手实践**：光学不练假把式
3. **及时复习**：艾宾浩斯记忆曲线
4. **记录笔记**：整理知识体系
5. **寻求帮助**：不懂就问社区

---

*计划生成时间：{generate_date}*
*祝学习顺利！*
"""
    
    def generate_plan(self,
                     topic: str,
                     main_goal: str,
                     duration_weeks: int = 12,
                     daily_hours: float = 2.0,
                     current_level: str = "零基础",
                     learning_mode: str = "自学",
                     start_date: Optional[datetime] = None) -> str:
        """生成学习计划"""
        
        if start_date is None:
            start_date = datetime.now()
        
        # 根据主题定制内容
        content_templates = self._get_content_by_topic(topic)
        
        end_date = start_date + timedelta(weeks=duration_weeks)
        
        # 计算各阶段周数
        phase1_weeks = min(2, duration_weeks // 4)
        phase2_weeks = duration_weeks // 2
        phase3_weeks = duration_weeks // 4
        phase4_weeks = duration_weeks - phase1_weeks - phase2_weeks - phase3_weeks
        
        return self.default_plan.format(
            topic=topic,
            main_goal=main_goal,
            secondary_goals="建立知识体系，能够独立实践应用",
            duration=f"{duration_weeks}周（约{duration_weeks//4}个月）",
            daily_hours=f"{daily_hours}小时",
            start_date=start_date.strftime("%Y年%m月%d日"),
            end_date=end_date.strftime("%Y年%m月%d日"),
            phase1_weeks=phase1_weeks,
            phase2_weeks=phase2_weeks,
            phase3_weeks=phase3_weeks,
            phase4_weeks=phase4_weeks,
            **content_templates,
            generate_date=datetime.now().strftime("%Y-%m-%d")
        )
    
    def _get_content_by_topic(self, topic: str) -> Dict:
        """根据主题获取内容模板"""
        topic_lower = topic.lower()
        
        if 'python' in topic_lower:
            return {
                'phase1_week1': 'Python环境搭建和基础语法',
                'phase1_task1': '完成Python安装，编写Hello World',
                'phase1_week2': '数据类型和运算符',
                'phase1_task2': '完成数据类型练习题',
                'phase2_week1': '控制流程（条件/循环）',
                'phase2_task1': '实现猜数字游戏',
                'phase2_week2': '函数和模块',
                'phase2_task2': '编写实用工具函数',
                'phase2_week3': '数据结构（列表/字典）',
                'phase2_task3': '实现数据处理脚本',
                'phase2_week4': '面向对象编程',
                'phase2_task4': '设计类并实现功能',
                'phase3_week1': '文件操作',
                'phase3_task1': '实现文件处理工具',
                'phase3_week2': '异常处理',
                'phase3_task2': '重构代码增加异常处理',
                'phase3_week3': '常用标准库',
                'phase3_task3': '使用datetime/json/re库',
                'phase3_week4': '第三方库',
                'phase3_task4': '安装和使用requests库',
                'resource1': '菜鸟教程Python3',
                'resource2': 'Python官方文档',
                'resource3': '《Python编程：从入门到实践》',
                'resource4': 'B站Python教程',
                'project1': '命令行TODO应用',
                'project2': '数据爬虫项目',
                'project3': '数据分析小工具',
                'time_slot1': '晚间19:00-20:30',
                'time_content1': '视频学习+笔记',
                'time_slot2': '晚间20:30-21:00',
                'time_content2': '动手练习'
            }
        else:
            # 默认模板
            return {
                'phase1_week1': '基础概念和背景知识',
                'phase1_task1': '完成基础知识梳理',
                'phase1_week2': '核心术语和框架',
                'phase1_task2': '整理术语表',
                'phase2_week1': '核心知识点一',
                'phase2_task1': '相关练习',
                'phase2_week2': '核心知识点二',
                'phase2_task2': '相关练习',
                'phase2_week3': '核心知识点三',
                'phase2_task3': '相关练习',
                'phase2_week4': '知识点整合',
                'phase2_task4': '综合练习',
                'phase3_week1': '进阶概念一',
                'phase3_task1': '进阶练习',
                'phase3_week2': '进阶概念二',
                'phase3_task2': '进阶练习',
                'phase3_week3': '最佳实践',
                'phase3_task3': '实践应用',
                'phase3_week4': '性能优化',
                'phase3_task4': '优化练习',
                'resource1': '官方文档',
                'resource2': '在线教程',
                'resource3': '经典书籍',
                'resource4': '视频课程',
                'project1': '小项目实践',
                'project2': '中等项目',
                'project3': '综合项目',
                'time_slot1': '固定时间段1',
                'time_content1': '知识学习',
                'time_slot2': '固定时间段2',
                'time_content2': '实践练习'
            }


if __name__ == "__main__":
    generator = LearningPlanGenerator()
    
    plan = generator.generate_plan(
        topic="Python编程",
        main_goal="3个月掌握Python基础，能够独立完成数据分析项目",
        duration_weeks=12,
        daily_hours=2.0,
        current_level="零基础"
    )
    
    print(plan)
