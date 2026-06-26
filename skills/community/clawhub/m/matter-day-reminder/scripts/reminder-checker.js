const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const { 
  getThisYearSolarDate, 
  getNextLunarBirthday, 
  parseLunarDate,
  formatLunarDate 
} = require('./lunar-converter');

/**
 * 提醒检查器
 * 检查今天需要提醒的事件
 */

class ReminderChecker {
  constructor(configPath = './config.yml') {
    this.config = this.loadConfig(configPath);
    this.contacts = [];
    this.reminders = [];
  }

  /**
   * 加载配置文件
   */
  loadConfig(configPath) {
    try {
      const configFile = fs.readFileSync(configPath, 'utf8');
      return yaml.load(configFile);
    } catch (error) {
      console.warn('配置文件加载失败，使用默认配置');
      return {
        data_path: './reminder-data',
        reminders: { enabled: true, advance_days: 7 }
      };
    }
  }

  /**
   * 加载所有联系人
   */
  loadContacts() {
    const contactsDir = path.join(this.config.data_path, 'contacts');
    
    if (!fs.existsSync(contactsDir)) {
      console.warn('联系人目录不存在');
      return [];
    }

    const files = fs.readdirSync(contactsDir).filter(f => f.endsWith('.md'));
    
    this.contacts = files.map(file => {
      const filePath = path.join(contactsDir, file);
      const content = fs.readFileSync(filePath, 'utf8');
      return this.parseContactFile(content, file);
    });

    return this.contacts;
  }

  /**
   * 解析联系人 Markdown 文件
   */
  parseContactFile(content, filename) {
    // 提取 YAML Frontmatter
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (!frontmatterMatch) {
      return null;
    }

    const frontmatter = yaml.load(frontmatterMatch[1]);
    
    // 解析事件部分
    const events = this.parseEvents(content);

    return {
      filename,
      ...frontmatter,
      events
    };
  }

  /**
   * 解析 Markdown 中的事件
   */
  parseEvents(content) {
    const events = [];
    
    // 匹配事件格式：### 事件名称 ...
    const eventRegex = /###\s+(.+?)\n([\s\S]*?)(?=###|$)/g;
    let match;
    
    while ((match = eventRegex.exec(content)) !== null) {
      const eventName = match[1].trim();
      const eventBody = match[2];
      
      // 提取事件详情
      const event = {
        name: eventName,
        type: this.extractField(eventBody, '类型'),
        date: this.extractField(eventBody, '日期'),
        isLunar: this.extractField(eventBody, '农历') === 'true',
        reminder: this.extractField(eventBody, '提醒') !== 'false'
      };
      
      events.push(event);
    }
    
    return events;
  }

  /**
   * 从文本中提取字段值
   */
  extractField(text, fieldName) {
    const regex = new RegExp(`\\*\\*${fieldName}\\*\\*[:：]\\s*(.+?)(?=\\n|$)`);
    const match = text.match(regex);
    return match ? match[1].trim() : null;
  }

  /**
   * 检查今天需要提醒的事件
   * @param {Date} checkDate - 检查的日期（默认为今天）
   * @returns {Array} 提醒列表
   */
  checkReminders(checkDate = new Date()) {
    this.reminders = [];
    const advanceDays = this.config.reminders?.advance_days || 7;

    this.contacts.forEach(contact => {
      if (!contact.events) return;

      contact.events.forEach(event => {
        if (!event.reminder) return;

        const reminderInfo = this.calculateReminder(contact, event, checkDate, advanceDays);
        
        if (reminderInfo) {
          this.reminders.push(reminderInfo);
        }
      });
    });

    return this.reminders;
  }

  /**
   * 计算提醒信息
   */
  calculateReminder(contact, event, checkDate, advanceDays) {
    const today = new Date(checkDate);
    today.setHours(0, 0, 0, 0);

    let targetDate;
    let isLunar = false;

    if (event.isLunar) {
      // 解析农历日期
      const lunarDate = parseLunarDate(event.date);
      if (!lunarDate) return null;

      // 获取下一个农历生日
      const nextBirthday = getNextLunarBirthday(lunarDate.month, lunarDate.day);
      targetDate = new Date(nextBirthday.year, nextBirthday.month - 1, nextBirthday.day);
      isLunar = true;
    } else {
      // 阳历日期
      const [year, month, day] = event.date.split('-').map(Number);
      const currentYear = today.getFullYear();
      
      // 今年的日期
      targetDate = new Date(currentYear, month - 1, day);
      
      // 如果今年的日期已过，使用明年的
      if (targetDate < today) {
        targetDate = new Date(currentYear + 1, month - 1, day);
      }
    }

    const daysUntil = Math.ceil((targetDate - today) / (1000 * 60 * 60 * 24));

    // 检查是否需要提醒（当天或提前7天）
    if (daysUntil === 0 || daysUntil === advanceDays) {
      return {
        contact: contact.name,
        relationship: contact.relationship,
        relationship_detail: contact.relationship_detail,
        event: event.name,
        event_type: event.type,
        target_date: targetDate.toISOString().split('T')[0],
        original_date: event.date,
        is_lunar: isLunar,
        days_until: daysUntil,
        reminder_type: daysUntil === 0 ? 'today' : 'advance',
        reminder_title: daysUntil === 0 
          ? `今天：${contact.name}的${event.name}`
          : `${advanceDays}天后：${contact.name}的${event.name}`
      };
    }

    return null;
  }

  /**
   * 获取格式化的提醒消息
   */
  getFormattedReminders() {
    if (this.reminders.length === 0) {
      return '今天没有需要提醒的事件。';
    }

    const todayReminders = this.reminders.filter(r => r.reminder_type === 'today');
    const advanceReminders = this.reminders.filter(r => r.reminder_type === 'advance');

    let message = '📅 **今日提醒**\n\n';

    if (todayReminders.length > 0) {
      message += '**今天：**\n';
      todayReminders.forEach((reminder, index) => {
        message += `${index + 1}. ${reminder.contact} 的 ${reminder.event}\n`;
        if (reminder.is_lunar) {
          message += `   农历：${reminder.original_date}\n`;
        }
        message += `   关系：${this.getRelationshipLabel(reminder.relationship)}\n\n`;
      });
    }

    if (advanceReminders.length > 0) {
      message += `**提前提醒（${this.config.reminders?.advance_days || 7}天后）：**\n`;
      advanceReminders.forEach((reminder, index) => {
        message += `${index + 1}. ${reminder.contact} 的 ${reminder.event}\n`;
        message += `   日期：${reminder.target_date}\n`;
        message += `   关系：${this.getRelationshipLabel(reminder.relationship)}\n\n`;
      });
    }

    return message;
  }

  /**
   * 获取关系标签
   */
  getRelationshipLabel(relationship) {
    const labels = {
      'friend': '朋友',
      'close_friend': '密友',
      'family': '家人',
      'colleague': '同事'
    };
    return labels[relationship] || relationship;
  }

  /**
   * 运行完整检查流程
   */
  run() {
    this.loadContacts();
    this.checkReminders();
    return {
      reminders: this.reminders,
      formatted: this.getFormattedReminders()
    };
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  const checker = new ReminderChecker();
  const result = checker.run();
  
  console.log(result.formatted);
  
  // 输出 JSON 格式的提醒数据（供其他脚本使用）
  console.log('\n---JSON_DATA---');
  console.log(JSON.stringify(result.reminders, null, 2));
}

module.exports = ReminderChecker;
