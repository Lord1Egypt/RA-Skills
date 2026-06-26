// 模拟 OpenClaw SDK 功能
class OpenClawSkill {
  constructor() {
    this.name = 'expense-tracker';
    this.version = '1.0.0';
  }
}

module.exports = { OpenClawSkill };
const fs = require('fs');
const path = require('path');

class ExpenseTrackerSkill {
  constructor() {
    this.dataFile = path.join(__dirname, 'data.json');
    this.categories = ['餐饮', '交通', '购物', '娱乐', '医疗', '其他'];
    this.loadData();
  }

  loadData() {
    try {
      if (fs.existsSync(this.dataFile)) {
        this.expenses = JSON.parse(fs.readFileSync(this.dataFile, 'utf8'));
      } else {
        this.expenses = [];
        this.saveData();
      }
    } catch (error) {
      console.error('加载数据失败:', error);
      this.expenses = [];
    }
  }

  saveData() {
    fs.writeFileSync(this.dataFile, JSON.stringify(this.expenses, null, 2));
  }

  parseExpense(text) {
    // 匹配中文数字和金额
    const amountMatch = text.match(/(\d+(?:\.\d+)?)元/);
    if (!amountMatch) {
      return null;
    }

    const amount = parseFloat(amountMatch[1]);
    let category = '其他';
    let description = text;

    // 智能分类
    if (text.includes('午饭') || text.includes('吃饭') || text.includes('餐厅')) {
      category = '餐饮';
    } else if (text.includes('打车') || text.includes('交通') || text.includes('地铁')) {
      category = '交通';
    } else if (text.includes('超市') || text.includes('购物') || text.includes('买')) {
      category = '购物';
    } else if (text.includes('电影') || text.includes('娱乐') || text.includes('游戏')) {
      category = '娱乐';
    } else if (text.includes('医疗') || text.includes('医院') || text.includes('药')) {
      category = '医疗';
    }

    // 提取描述
    description = description.replace(/(\d+(?:\.\d+)?)元/, '').trim();

    return {
      id: Date.now().toString(),
      amount,
      category,
      description,
      date: new Date().toISOString().split('T')[0],
      timestamp: Date.now()
    };
  }

  addExpense(expense) {
    this.expenses.push(expense);
    this.saveData();
    return expense;
  }

  getStatistics(period = 'month') {
    const now = new Date();
    const stats = {
      total: 0,
      byCategory: {},
      byDate: {},
      count: 0
    };

    this.expenses.forEach(expense => {
      const expenseDate = new Date(expense.date);
      let include = false;

      switch (period) {
        case 'day':
          include = expenseDate.toDateString() === now.toDateString();
          break;
        case 'week':
          const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
          include = expenseDate >= weekAgo;
          break;
        case 'month':
          include = expenseDate.getMonth() === now.getMonth() &&
                   expenseDate.getFullYear() === now.getFullYear();
          break;
      }

      if (include) {
        stats.total += expense.amount;
        stats.count++;

        // 按类别统计
        if (!stats.byCategory[expense.category]) {
          stats.byCategory[expense.category] = 0;
        }
        stats.byCategory[expense.category] += expense.amount;

        // 按日期统计
        if (!stats.byDate[expense.date]) {
          stats.byDate[expense.date] = 0;
        }
        stats.byDate[expense.date] += expense.amount;
      }
    });

    return stats;
  }

  handleMessage(message) {
    const text = message.content.toLowerCase();

    if (text.includes('记账') || text.includes('记录') || text.includes('添加')) {
      const expense = this.parseExpense(message.content);
      if (expense) {
        const savedExpense = this.addExpense(expense);
        return `✅ 记账成功！\n💵 金额: ¥${savedExpense.amount}\n📂 分类: ${savedExpense.category}\n📝 备注: ${savedExpense.description || '无'}\n📅 日期: ${savedExpense.date}`;
      } else {
        return '❌ 无法解析金额，请按格式："记账：项目 金额元"';
      }
    }

    if (text.includes('查询') || text.includes('统计')) {
      const period = text.includes('这个月') ? 'month' :
                    text.includes('本周') ? 'week' :
                    text.includes('今天') ? 'day' : 'month';

      const stats = this.getStatistics(period);
      const periodNames = { day: '今天', week: '本周', month: '本月' };
      const periodName = periodNames[period];

      let response = `📊 ${periodName}支出统计：\n💰 总支出: ¥${stats.total.toFixed(2)}\n📈 记账笔数: ${stats.count}`;

      if (Object.keys(stats.byCategory).length > 0) {
        response += '\n📂 按类别分布：';
        Object.entries(stats.byCategory).forEach(([category, amount]) => {
          const percentage = stats.total > 0 ? ((amount / stats.total) * 100).toFixed(1) : 0;
          response += `\n  ${category}: ¥${amount.toFixed(2)} (${percentage}%)`;
        });
      }

      return response;
    }

    if (text.includes('列表') || text.includes('明细')) {
      const recentExpenses = this.expenses.slice(-10).reverse();
      if (recentExpenses.length === 0) {
        return '📋 暂无记账记录';
      }

      let response = '📋 最近记账记录：\n';
      recentExpenses.forEach(expense => {
        response += `\n${expense.date} | ${expense.category} | ¥${expense.amount} | ${expense.description || '无'}\n`;
      });
      return response;
    }

    return '🤔 我不太明白，试试：\n• "记账：项目 金额元"\n• "查询：这个月花了多少钱"\n• "统计：本月支出"\n• "列表：查看记录"';
  }
}

module.exports = ExpenseTrackerSkill;