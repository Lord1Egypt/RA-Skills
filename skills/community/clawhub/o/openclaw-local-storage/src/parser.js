class Parser {
  parseCommand(command) {
    // 分析操作类型
    if (command.includes('添加')) {
      return this.parseAddCommand(command);
    } else if (command.includes('查询')) {
      return this.parseQueryCommand(command);
    } else if (command.includes('修改')) {
      return this.parseUpdateCommand(command);
    } else if (command.includes('删除')) {
      return this.parseDeleteCommand(command);
    }
    return null;
  }

  parseAddCommand(command) {
    // 解析添加命令，格式：添加一条[类型]信息：字段1为值1，字段2为值2
    const dataMatch = command.match(/添加一条.*：(.*)/);
    if (!dataMatch) return null;

    const dataStr = dataMatch[1];
    const data = {};

    // 提取字段和值
    const fieldMatches = dataStr.match(/([^，]+)为([^，]+)/g);
    if (!fieldMatches) return null;

    fieldMatches.forEach(match => {
      const [field, value] = match.split('为');
      // 尝试转换值的类型
      let parsedValue = value;
      if (!isNaN(value) && value.trim() !== '') {
        parsedValue = Number(value);
      } else if (value === 'true') {
        parsedValue = true;
      } else if (value === 'false') {
        parsedValue = false;
      }
      data[field.trim()] = parsedValue;
    });

    return {
      action: 'add',
      data
    };
  }

  parseQueryCommand(command) {
    // 解析查询命令，格式：查询所有[类型]信息 或 查询字段为值的[类型]信息
    if (command.includes('所有')) {
      return {
        action: 'query',
        conditions: {}
      };
    }

    // 解析条件查询
    const conditionMatch = command.match(/查询([^的]+)为([^的]+)的/);
    if (conditionMatch) {
      const [, field, value] = conditionMatch;
      // 尝试转换值的类型
      let parsedValue = value;
      if (!isNaN(value) && value.trim() !== '') {
        parsedValue = Number(value);
      } else if (value === 'true') {
        parsedValue = true;
      } else if (value === 'false') {
        parsedValue = false;
      }

      return {
        action: 'query',
        conditions: {
          [field.trim()]: parsedValue
        }
      };
    }

    return null;
  }

  parseUpdateCommand(command) {
    // 解析修改命令，格式：修改字段为值的[类型]信息，字段改为值
    const conditionMatch = command.match(/修改([^的]+)为([^的]+)的.*，(.*)/);
    if (!conditionMatch) return null;

    const [, conditionField, conditionValue, dataStr] = conditionMatch;
    
    // 解析条件
    let parsedConditionValue = conditionValue;
    if (!isNaN(conditionValue) && conditionValue.trim() !== '') {
      parsedConditionValue = Number(conditionValue);
    } else if (conditionValue === 'true') {
      parsedConditionValue = true;
    } else if (conditionValue === 'false') {
      parsedConditionValue = false;
    }

    // 解析要修改的数据
    const data = {};
    const dataMatches = dataStr.match(/([^，]+)改为([^，]+)/g);
    if (!dataMatches) return null;

    dataMatches.forEach(match => {
      const [field, value] = match.split('改为');
      // 尝试转换值的类型
      let parsedValue = value;
      if (!isNaN(value) && value.trim() !== '') {
        parsedValue = Number(value);
      } else if (value === 'true') {
        parsedValue = true;
      } else if (value === 'false') {
        parsedValue = false;
      }
      data[field.trim()] = parsedValue;
    });

    return {
      action: 'update',
      conditions: {
        [conditionField.trim()]: parsedConditionValue
      },
      data
    };
  }

  parseDeleteCommand(command) {
    // 解析删除命令，格式：删除字段为值的[类型]信息
    const conditionMatch = command.match(/删除([^的]+)为([^的]+)的/);
    if (!conditionMatch) return null;

    const [, field, value] = conditionMatch;
    // 尝试转换值的类型
    let parsedValue = value;
    if (!isNaN(value) && value.trim() !== '') {
      parsedValue = Number(value);
    } else if (value === 'true') {
      parsedValue = true;
    } else if (value === 'false') {
      parsedValue = false;
    }

    return {
      action: 'delete',
      conditions: {
        [field.trim()]: parsedValue
      }
    };
  }
}

module.exports = Parser;