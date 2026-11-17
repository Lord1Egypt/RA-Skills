import tempfile
from openclaw.skill import Skill
import pandas as pd
import matplotlib.pyplot as plt
import os

# 技能启动时一次性加载csv数据
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "sales.csv"))

class DataAnalyzerSkill(Skill):
    def __init__(self):
        super().__init__()
        self.df = df

    def query_sales_data(self, question: str) -> str:
        """数据查询实现"""
        q = question.lower()
        if "最高" in q or "最大" in q:
            if "销售额" in q:
                max_row = self.df.loc[self.df['sales'].idxmax()]
                return f"销售额最高的记录是{max_row['month']}月,{max_row['region']}地区,{max_row['product']}产品,销售额为{max_row['sales']}"
            elif "利润" in q:
                max_row = self.df.loc[self.df['profit'].idxmax()]
                return f"利润最高的记录是{max_row['month']}月,{max_row['region']}地区,利润为{max_row['profit']}"
        if "总销售额" in q:
            total = self.df['sales'].sum()
            return f"总销售额为{total}"
        if "总利润" in q:
            total = self.df['profit'].sum()
            return f"总利润为{total}"
        return f"无法理解:{question}"

    def plot_sales_data(self, chart_type: str = "line", metric: str = "sales") -> str:
        """绘图实现"""
        plt.figure(figsize=(10, 6))
        if chart_type == "line":
            monthly = self.df.groupby('month')[metric].sum()
            monthly.plot(kind='line', marker='o')
            plt.title(f"Monthly {metric.capitalize()} Trend")
        elif chart_type == "bar":
            regional = self.df.groupby('region')[metric].sum()
            regional.plot(kind='bar')
            plt.title(f"{metric.capitalize()} by Region")
        else:
            return f"不支持的图表类型:{chart_type}"
        img_path = os.path.join(tempfile.gettempdir(), f"sales_{metric}_{chart_type}.png")
        plt.savefig(img_path)
        plt.close()
        return f"图表已保存为{img_path}"

    def analyze_sales_trend(self, question: str) -> str:
        """分析实现"""
        q = question.lower()
        if "利润下降" in q or "利润为什么" in q:
            monthly_profit = self.df.groupby('month')['profit'].sum()
            if len(monthly_profit) >= 2:
                months = list(monthly_profit.index)
                changes = []
                for i in range(1, len(months)):
                    change = monthly_profit.iloc[i] - monthly_profit.iloc[i-1]
                    changes.append(f"{months[i]}月相比{months[i-1]}月:{change}")
                return f"利润变化趋势:\n" + "\n".join(changes)
        return f"请提供更具体的分析问题。"

# 框架自动加载技能实例约定
skill = DataAnalyzerSkill()