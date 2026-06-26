const fs = require('fs');
const path = require('path');

class Storage {
  constructor() {
    this.dataFile = path.join(__dirname, '../data.json');
    this.fields = {};
  }

  async init(fields) {
    this.fields = fields;
    // 确保数据文件存在
    if (!fs.existsSync(this.dataFile)) {
      await this.saveData([]);
    }
  }

  async add(data) {
    try {
      const currentData = await this.loadData();
      currentData.push(data);
      await this.saveData(currentData);
      return '数据添加成功';
    } catch (error) {
      return '数据添加失败：' + error.message;
    }
  }

  async query(conditions = {}) {
    try {
      const data = await this.loadData();
      if (Object.keys(conditions).length === 0) {
        return JSON.stringify(data, null, 2);
      }

      const filtered = data.filter(item => {
        return Object.entries(conditions).every(([key, value]) => {
          return item[key] === value;
        });
      });

      return JSON.stringify(filtered, null, 2);
    } catch (error) {
      return '查询失败：' + error.message;
    }
  }

  async update(conditions, data) {
    try {
      const currentData = await this.loadData();
      let updated = false;

      const newData = currentData.map(item => {
        const match = Object.entries(conditions).every(([key, value]) => {
          return item[key] === value;
        });

        if (match) {
          updated = true;
          return { ...item, ...data };
        }
        return item;
      });

      if (updated) {
        await this.saveData(newData);
        return '数据更新成功';
      } else {
        return '未找到匹配的数据';
      }
    } catch (error) {
      return '更新失败：' + error.message;
    }
  }

  async delete(conditions) {
    try {
      const currentData = await this.loadData();
      const newData = currentData.filter(item => {
        return !Object.entries(conditions).every(([key, value]) => {
          return item[key] === value;
        });
      });

      if (newData.length < currentData.length) {
        await this.saveData(newData);
        return '数据删除成功';
      } else {
        return '未找到匹配的数据';
      }
    } catch (error) {
      return '删除失败：' + error.message;
    }
  }

  async loadData() {
    if (!fs.existsSync(this.dataFile)) {
      return [];
    }

    const data = fs.readFileSync(this.dataFile, 'utf8');
    return JSON.parse(data);
  }

  async saveData(data) {
    fs.writeFileSync(this.dataFile, JSON.stringify(data, null, 2), 'utf8');
  }
}

module.exports = Storage;