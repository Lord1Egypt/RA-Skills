/**
 * Database 单元测试
 */

const { Database } = require('../db/database');

// 模拟数据库连接
class MockDB {
  constructor() {
    this.data = {
      users: [],
      agents: [],
      tasks: []
    };
    this.queryCount = 0;
  }

  async query(sql, params = []) {
    this.queryCount++;
    // 简化实现，仅用于测试
    if (sql.includes('SELECT') && sql.includes('users')) {
      return this.data.users;
    }
    if (sql.includes('INSERT') && sql.includes('users')) {
      const id = this.data.users.length + 1;
      this.data.users.push({ id, ...params });
      return { insertId: id };
    }
    return [];
  }

  async insert(table, data) {
    const id = this.data[table].length + 1;
    const record = { id, ...data };
    this.data[table].push(record);
    return { insertId: id, lastInsertRowid: id };
  }

  // 同步版本
  insertSync(table, data) {
    const id = this.data[table].length + 1;
    const record = { id, ...data };
    this.data[table].push(record);
    return { insertId: id, lastInsertRowid: id };
  }

  async select(table, where = {}) {
    return this.data[table].filter((item) => {
      return Object.entries(where).every(([key, value]) => item[key] === value);
    });
  }

  async update(table, data, where) {
    const index = this.data[table].findIndex((item) => {
      return Object.entries(where).every(([key, value]) => item[key] === value);
    });
    if (index !== -1) {
      this.data[table][index] = { ...this.data[table][index], ...data };
      return { changes: 1 };
    }
    return { changes: 0 };
  }

  async delete(table, where) {
    const initialLength = this.data[table].length;
    this.data[table] = this.data[table].filter((item) => {
      return !Object.entries(where).every(([key, value]) => item[key] === value);
    });
    return { changes: initialLength - this.data[table].length };
  }

  close() {
    this.data = {};
  }

  async closeAsync() {
    this.data = {};
  }

  // 模拟 better-sqlite3 的 prepare 方法
  prepare(sql) {
    const self = this;
    const queryInfo = { sql, params: [] };

    return {
      run(...params) {
        queryInfo.params = params;
        // 解析 SQL 类型
        if (sql.includes('INSERT')) {
          const tableMatch = sql.match(/INSERT INTO (\w+)/);
          const table = tableMatch ? tableMatch[1] : 'users';
          // 根据表类型构建数据对象
          if (table === 'users') {
            const data = {
              username: params[0],
              email: params[1],
              password: params[2],
              role: params[3],
              status: params[4]
            };
            const result = self.insertSync(table, data);
            return { lastInsertRowid: result.insertId, changes: 1 };
          } else if (table === 'agents') {
            const data = {
              name: params[0],
              status: params[1],
              current_task_id: params[2],
              last_heartbeat: params[3],
              ip_address: params[4]
            };
            const result = self.insertSync(table, data);
            return { lastInsertRowid: result.insertId, changes: 1 };
          } else if (table === 'tasks') {
            const data = {
              title: params[0],
              description: params[1],
              priority: params[2],
              status: params[3],
              assignee_id: params[4],
              created_at: params[5] || new Date().toISOString(),
              updated_at: params[6] || new Date().toISOString()
            };
            const result = self.insertSync(table, data);
            return { lastInsertRowid: result.insertId, changes: 1 };
          }
          return { lastInsertRowid: 0, changes: 0 };
        } else if (sql.includes('UPDATE')) {
          const tableMatch = sql.match(/UPDATE (\w+)/);
          const table = tableMatch ? tableMatch[1] : 'users';

          // 解析 WHERE id = ?
          if (sql.includes('WHERE id = ?')) {
            const id = params[params.length - 1]; // 最后一个参数是 WHERE 条件
            const updateData = {};

            // 处理字符串常量值 (如 status = 'in_progress' 或 status = "in_progress")
            const statusMatch = sql.match(/status = ['"]([^'"]+)['"]/);
            if (statusMatch) {
              updateData.status = statusMatch[1];
            }

            // 根据 SQL 中的字段设置更新数据
            const fields = [];
            if (sql.includes('email = ?')) fields.push('email');
            if (sql.includes('password = ?')) fields.push('password');
            if (sql.includes('status = ?')) fields.push('status');
            if (sql.includes('name = ?')) fields.push('name');
            if (sql.includes('last_heartbeat = ?')) fields.push('last_heartbeat');
            if (sql.includes('current_task_id = ?')) fields.push('current_task_id');
            if (sql.includes('assignee_id = ?')) fields.push('assignee_id');
            if (sql.includes('title = ?')) fields.push('title');

            // 根据字段顺序分配参数值
            let paramIndex = 0;
            if (fields.includes('email')) updateData.email = params[paramIndex++];
            if (fields.includes('password')) updateData.password = params[paramIndex++];
            if (fields.includes('status') && !updateData.status)
              updateData.status = params[paramIndex++];
            if (fields.includes('name')) updateData.name = params[paramIndex++];
            if (fields.includes('last_heartbeat')) updateData.last_heartbeat = params[paramIndex++];
            if (fields.includes('current_task_id'))
              updateData.current_task_id = params[paramIndex++];
            if (fields.includes('assignee_id')) updateData.assignee_id = params[paramIndex++];
            if (fields.includes('title')) updateData.title = params[paramIndex++];

            const index = self.data[table].findIndex((item) => item.id === id);
            if (index !== -1) {
              self.data[table][index] = { ...self.data[table][index], ...updateData };
              return { changes: 1 };
            }
            return { changes: 0 };
          }
          return { changes: 0 };
        } else if (sql.includes('DELETE')) {
          const tableMatch = sql.match(/DELETE FROM (\w+)/);
          const table = tableMatch ? tableMatch[1] : 'users';

          if (sql.includes('WHERE id = ?')) {
            const id = params[0];
            const initialLength = self.data[table].length;
            self.data[table] = self.data[table].filter((item) => item.id !== id);
            return { changes: initialLength - self.data[table].length };
          }
          return { changes: 0 };
        }
        return { changes: 0 };
      },
      get: function (...params) {
        queryInfo.params = params;
        const tableMatch = sql.match(/FROM (\w+)/);
        const table = tableMatch ? tableMatch[1] : 'users';

        // 处理 SUM() for statistics (优先处理，因为包含 COUNT(*) 和 SUM(CASE))
        if (sql.includes('SUM(CASE')) {
          // 处理任务统计查询
          const total = self.data[table].length;
          const pending = self.data[table].filter((t) => t.status === 'pending').length;
          const inProgress = self.data[table].filter((t) => t.status === 'in_progress').length;
          const completed = self.data[table].filter((t) => t.status === 'completed').length;
          return { total, pending, in_progress: inProgress, completed };
        }

        // 处理 WHERE id = ?
        if (sql.includes('WHERE id = ?')) {
          const id = params[0];
          const result = self.data[table].find((item) => item.id === id);
          return result || null;
        }

        // 处理 WHERE email = ?
        if (sql.includes('WHERE email = ?')) {
          const email = params[0];
          return self.data[table].find((item) => item.email === email) || null;
        }

        // 处理 WHERE username = ?
        if (sql.includes('WHERE username = ?')) {
          const username = params[0];
          return self.data[table].find((item) => item.username === username) || null;
        }

        // 处理 WHERE name = ?
        if (sql.includes('WHERE name = ?')) {
          const name = params[0];
          return self.data[table].find((item) => item.name === name) || null;
        }

        // 处理 WHERE status = ?
        if (sql.includes('WHERE status = ?')) {
          const status = params[0];
          return self.data[table].find((item) => item.status === status) || null;
        }

        // 处理 SELECT * FROM tasks (无 WHERE)
        if (sql.includes('SELECT * FROM tasks') && !sql.includes('WHERE')) {
          return [...self.data.tasks];
        }

        // 处理 COUNT(*)
        if (sql.includes('COUNT(*)')) {
          let count = self.data[table].length;

          // 处理 WHERE 条件
          if (sql.includes("WHERE status = 'pending'") && !sql.includes('AND')) {
            count = self.data[table].filter((item) => item.status === 'pending').length;
          } else if (sql.includes("WHERE status = 'in_progress'") && !sql.includes('AND')) {
            count = self.data[table].filter((item) => item.status === 'in_progress').length;
          } else if (sql.includes("WHERE status = 'completed'") && !sql.includes('AND')) {
            count = self.data[table].filter((item) => item.status === 'completed').length;
          } else if (sql.includes("WHERE status = 'idle'") && !sql.includes('AND')) {
            count = self.data[table].filter((item) => item.status === 'idle').length;
          } else if (sql.includes("WHERE status = 'busy'") && !sql.includes('AND')) {
            count = self.data[table].filter((item) => item.status === 'busy').length;
          } else if (sql.includes('WHERE status = ?')) {
            const status = params[0];
            count = self.data[table].filter((item) => item.status === status).length;
          }
          // 如果没有 WHERE 条件，返回总数
          else if (!sql.includes('WHERE')) {
            count = self.data[table].length;
          }
          // 默认返回总数（处理其他情况）
          else {
            count = self.data[table].length;
          }

          return { count };
        }

        return null;
      },
      all: function (...params) {
        queryInfo.params = params;
        const tableMatch = sql.match(/SELECT \* FROM (\w+)/);
        const table = tableMatch ? tableMatch[1] : 'users';

        let results = [...self.data[table]];

        // 处理 WHERE status = 'pending' AND assignee_id IS NULL (优先处理复杂条件)
        if (sql.includes("WHERE status = 'pending' AND assignee_id IS NULL")) {
          results = results.filter(
            (item) =>
              item.status === 'pending' &&
              (item.assignee_id === null || item.assignee_id === undefined)
          );
        }
        // 处理 WHERE status = 'idle'
        else if (sql.includes("WHERE status = 'idle'")) {
          results = results.filter((item) => item.status === 'idle');
        }
        // 处理 WHERE status = 'busy'
        else if (sql.includes("WHERE status = 'busy'")) {
          results = results.filter((item) => item.status === 'busy');
        }
        // 处理 WHERE status = 'pending' (单独)
        else if (sql.includes("WHERE status = 'pending'") && !sql.includes('AND')) {
          results = results.filter((item) => item.status === 'pending');
        }
        // 处理 WHERE status = 'in_progress' (单独)
        else if (sql.includes("WHERE status = 'in_progress'") && !sql.includes('AND')) {
          results = results.filter((item) => item.status === 'in_progress');
        }
        // 处理 WHERE status = 'completed' (单独)
        else if (sql.includes("WHERE status = 'completed'") && !sql.includes('AND')) {
          results = results.filter((item) => item.status === 'completed');
        }
        // 处理 WHERE status = ?
        else if (sql.includes('WHERE status = ?')) {
          const status = params[0];
          results = results.filter((item) => item.status === status);
        }
        // 处理 WHERE assignee_id = ?
        else if (sql.includes('WHERE assignee_id = ?')) {
          const assigneeId = params[0];
          results = results.filter((item) => item.assignee_id === assigneeId);
        }
        // 处理 WHERE assignee_id IS NULL
        else if (sql.includes('WHERE assignee_id IS NULL')) {
          results = results.filter(
            (item) => item.assignee_id === null || item.assignee_id === undefined
          );
        }
        // 处理 WHERE status = ? AND assignee_id IS NULL
        else if (sql.includes('WHERE status = ?') && sql.includes('AND assignee_id IS NULL')) {
          const status = params[0];
          results = results.filter(
            (item) =>
              item.status === status &&
              (item.assignee_id === null || item.assignee_id === undefined)
          );
        }

        return results;
      }
    };
  }
}

describe('Database - 数据库操作', () => {
  let db;
  let mockDB;

  beforeEach(() => {
    mockDB = new MockDB();
    db = new Database(mockDB);
  });

  afterEach(async () => {
    await db.close();
  });

  describe('用户操作', () => {
    test('应该创建用户', async () => {
      const user = {
        username: 'testuser',
        email: 'test@example.com',
        password: 'hashed_password',
        role: 'user',
        status: 'active'
      };

      const result = await db.createUser(user);
      expect(result).toBeDefined();
      expect(result.id).toBe(1);
      expect(result.username).toBe('testuser');
    });

    test('应该获取用户列表', async () => {
      await db.createUser({
        username: 'user1',
        email: 'user1@test.com',
        password: 'pass',
        role: 'user',
        status: 'active'
      });
      await db.createUser({
        username: 'user2',
        email: 'user2@test.com',
        password: 'pass',
        role: 'user',
        status: 'active'
      });

      const users = await db.getUsers();
      expect(users.length).toBe(2);
    });

    test('应该获取特定用户', async () => {
      const user = await db.createUser({
        username: 'testuser',
        email: 'test@test.com',
        password: 'pass',
        role: 'user',
        status: 'active'
      });
      const foundUser = await db.getUser(user.id);

      expect(foundUser).toBeDefined();
      expect(foundUser.username).toBe('testuser');
    });

    test('应该更新用户', async () => {
      const user = await db.createUser({
        username: 'testuser',
        email: 'test@test.com',
        password: 'pass',
        role: 'user',
        status: 'active'
      });

      const updated = await db.updateUser(user.id, { email: 'updated@test.com' });
      expect(updated.changes).toBe(1);

      const foundUser = await db.getUser(user.id);
      expect(foundUser.email).toBe('updated@test.com');
    });

    test('应该删除用户', async () => {
      const user = await db.createUser({
        username: 'testuser',
        email: 'test@test.com',
        password: 'pass',
        role: 'user',
        status: 'active'
      });

      const result = await db.deleteUser(user.id);
      expect(result.changes).toBe(1);

      const foundUser = await db.getUser(user.id);
      expect(foundUser).toBeNull();
    });

    test('应该根据用户名获取用户', async () => {
      await db.createUser({
        username: 'testuser',
        email: 'test@test.com',
        password: 'pass',
        role: 'user',
        status: 'active'
      });

      const user = await db.getUserByUsername('testuser');
      expect(user.username).toBe('testuser');
    });

    test('应该根据邮箱获取用户', async () => {
      await db.createUser({
        username: 'testuser',
        email: 'test@test.com',
        password: 'pass',
        role: 'user',
        status: 'active'
      });

      const user = await db.getUserByEmail('test@test.com');
      expect(user.email).toBe('test@test.com');
    });

    test('应该更新用户密码', async () => {
      const user = await db.createUser({
        username: 'testuser',
        email: 'test@test.com',
        password: 'oldpass',
        role: 'user',
        status: 'active'
      });

      await db.updateUserPassword(user.id, 'newpassword');
      const updated = await db.getUser(user.id);
      expect(updated.password).toBe('newpassword');
    });

    test('应该更新用户状态', async () => {
      const user = await db.createUser({
        username: 'testuser',
        email: 'test@test.com',
        password: 'pass',
        role: 'user',
        status: 'active'
      });

      await db.updateUserStatus(user.id, 'inactive');
      const updated = await db.getUser(user.id);
      expect(updated.status).toBe('inactive');
    });
  });

  describe('Agent 操作', () => {
    test('应该创建 Agent', async () => {
      const agent = {
        name: 'test-agent',
        status: 'idle',
        current_task_id: null,
        last_heartbeat: new Date().toISOString(),
        ip_address: '127.0.0.1'
      };

      const result = await db.createAgent(agent);
      expect(result).toBeDefined();
      expect(result.id).toBe(1);
      expect(result.name).toBe('test-agent');
    });

    test('应该获取 Agent 列表', async () => {
      await db.createAgent({
        name: 'agent1',
        status: 'idle',
        current_task_id: null,
        last_heartbeat: new Date().toISOString(),
        ip_address: '127.0.0.1'
      });
      await db.createAgent({
        name: 'agent2',
        status: 'busy',
        current_task_id: null,
        last_heartbeat: new Date().toISOString(),
        ip_address: '127.0.0.2'
      });

      const agents = await db.getAgents();
      expect(agents.length).toBe(2);
    });

    test('应该获取特定 Agent', async () => {
      const agent = await db.createAgent({
        name: 'test-agent',
        status: 'idle',
        current_task_id: null,
        last_heartbeat: new Date().toISOString(),
        ip_address: '127.0.0.1'
      });
      const foundAgent = await db.getAgent(agent.id);

      expect(foundAgent).toBeDefined();
      expect(foundAgent.name).toBe('test-agent');
    });

    test('应该更新 Agent 状态', async () => {
      const agent = await db.createAgent({
        name: 'test-agent',
        status: 'idle',
        current_task_id: null,
        last_heartbeat: new Date().toISOString(),
        ip_address: '127.0.0.1'
      });

      await db.updateAgentStatus(agent.id, 'busy');
      const updated = await db.getAgent(agent.id);
      expect(updated.status).toBe('busy');
    });

    test('应该更新 Agent 心跳', async () => {
      const agent = await db.createAgent({
        name: 'test-agent',
        status: 'idle',
        current_task_id: null,
        last_heartbeat: new Date().toISOString(),
        ip_address: '127.0.0.1'
      });
      const oldHeartbeat = agent.last_heartbeat;

      await new Promise((resolve) => setTimeout(resolve, 10));
      await db.updateAgentHeartbeat(agent.id);
      const updated = await db.getAgent(agent.id);
      expect(updated.last_heartbeat).not.toBe(oldHeartbeat);
    });

    test('应该更新 Agent 当前任务', async () => {
      const agent = await db.createAgent({
        name: 'test-agent',
        status: 'idle',
        current_task_id: null,
        last_heartbeat: new Date().toISOString(),
        ip_address: '127.0.0.1'
      });

      await db.updateAgentCurrentTask(agent.id, 123);
      const updated = await db.getAgent(agent.id);
      expect(updated.current_task_id).toBe(123);
    });

    test('应该获取空闲 Agent', async () => {
      await db.createAgent({
        name: 'agent1',
        status: 'idle',
        current_task_id: null,
        last_heartbeat: new Date().toISOString(),
        ip_address: '127.0.0.1'
      });
      await db.createAgent({
        name: 'agent2',
        status: 'busy',
        current_task_id: null,
        last_heartbeat: new Date().toISOString(),
        ip_address: '127.0.0.2'
      });

      const idleAgents = await db.getIdleAgents();
      expect(idleAgents.length).toBe(1);
      expect(idleAgents[0].name).toBe('agent1');
    });

    test('应该删除 Agent', async () => {
      const agent = await db.createAgent({
        name: 'test-agent',
        status: 'idle',
        current_task_id: null,
        last_heartbeat: new Date().toISOString(),
        ip_address: '127.0.0.1'
      });

      const result = await db.deleteAgent(agent.id);
      expect(result.changes).toBe(1);

      const foundAgent = await db.getAgent(agent.id);
      expect(foundAgent).toBeNull();
    });
  });

  describe('任务操作', () => {
    test('应该创建任务', async () => {
      const task = {
        title: 'Test Task',
        description: 'Task description',
        priority: 1,
        status: 'pending',
        assignee_id: null
      };

      const result = await db.createTask(task);
      expect(result).toBeDefined();
      expect(result.id).toBe(1);
      expect(result.title).toBe('Test Task');
    });

    test('应该获取任务列表', async () => {
      await db.createTask({
        title: 'Task 1',
        description: 'Desc 1',
        priority: 1,
        status: 'pending',
        assignee_id: null
      });
      await db.createTask({
        title: 'Task 2',
        description: 'Desc 2',
        priority: 2,
        status: 'pending',
        assignee_id: null
      });

      const tasks = await db.getTasks();
      expect(tasks.length).toBe(2);
    });

    test('应该获取特定任务', async () => {
      const task = await db.createTask({
        title: 'Test Task',
        description: 'Desc',
        priority: 1,
        status: 'pending',
        assignee_id: null
      });
      const foundTask = await db.getTask(task.id);

      expect(foundTask).toBeDefined();
      expect(foundTask.title).toBe('Test Task');
    });

    test('应该更新任务状态', async () => {
      const task = await db.createTask({
        title: 'Test Task',
        description: 'Desc',
        priority: 1,
        status: 'pending',
        assignee_id: null
      });

      await db.updateTaskStatus(task.id, 'in_progress');
      const updated = await db.getTask(task.id);
      expect(updated.status).toBe('in_progress');
    });

    test('应该分配任务给 Agent', async () => {
      const task = await db.createTask({
        title: 'Test Task',
        description: 'Desc',
        priority: 1,
        status: 'pending',
        assignee_id: null
      });
      const agent = await db.createAgent({
        name: 'test-agent',
        status: 'idle',
        current_task_id: null,
        last_heartbeat: new Date().toISOString(),
        ip_address: '127.0.0.1'
      });

      await db.assignTask(task.id, agent.id);
      const updatedTask = await db.getTask(task.id);
      expect(updatedTask.assignee_id).toBe(agent.id);
      expect(updatedTask.status).toBe('in_progress');
    });

    test('应该删除任务', async () => {
      const task = await db.createTask({
        title: 'Test Task',
        description: 'Desc',
        priority: 1,
        status: 'pending',
        assignee_id: null
      });

      const result = await db.deleteTask(task.id);
      expect(result.changes).toBe(1);

      const foundTask = await db.getTask(task.id);
      expect(foundTask).toBeNull();
    });

    test('应该获取待分配任务', async () => {
      await db.createTask({
        title: 'Task 1',
        description: 'Desc 1',
        priority: 1,
        status: 'pending',
        assignee_id: null
      });
      await db.createTask({
        title: 'Task 2',
        description: 'Desc 2',
        priority: 2,
        status: 'in_progress',
        assignee_id: 1
      });

      const pendingTasks = await db.getPendingTasks();
      expect(pendingTasks.length).toBe(1);
      expect(pendingTasks[0].title).toBe('Task 1');
    });

    test('应该获取 Agent 的任务', async () => {
      const agent = await db.createAgent({
        name: 'test-agent',
        status: 'idle',
        current_task_id: null,
        last_heartbeat: new Date().toISOString(),
        ip_address: '127.0.0.1'
      });
      await db.createTask({
        title: 'Task 1',
        description: 'Desc 1',
        priority: 1,
        status: 'in_progress',
        assignee_id: agent.id
      });
      await db.createTask({
        title: 'Task 2',
        description: 'Desc 2',
        priority: 2,
        status: 'in_progress',
        assignee_id: agent.id
      });

      const tasks = await db.getAgentTasks(agent.id);
      expect(tasks.length).toBe(2);
    });

    test('应该获取任务统计', async () => {
      await db.createTask({
        title: 'Task 1',
        description: 'Desc',
        priority: 1,
        status: 'pending',
        assignee_id: null
      });
      await db.createTask({
        title: 'Task 2',
        description: 'Desc',
        priority: 2,
        status: 'in_progress',
        assignee_id: 1
      });
      await db.createTask({
        title: 'Task 3',
        description: 'Desc',
        priority: 3,
        status: 'completed',
        assignee_id: 1
      });

      const stats = await db.getTaskStats();
      expect(stats).toBeDefined();
      expect(stats.total).toBe(3);
      expect(stats.pending).toBe(1);
      expect(stats.in_progress).toBe(1);
      expect(stats.completed).toBe(1);
    });
  });

  describe('错误处理', () => {
    test('应该处理无效的用户名', async () => {
      await expect(
        db.createUser({
          username: '',
          email: 'test@test.com',
          password: 'pass',
          role: 'user',
          status: 'active'
        })
      ).rejects.toThrow();
    });

    test('应该处理无效的邮箱', async () => {
      await expect(
        db.createUser({
          username: 'testuser',
          email: 'invalid',
          password: 'pass',
          role: 'user',
          status: 'active'
        })
      ).rejects.toThrow();
    });

    test('应该处理无效的 Agent 名称', async () => {
      await expect(
        db.createAgent({
          name: '',
          status: 'idle',
          current_task_id: null,
          last_heartbeat: new Date().toISOString(),
          ip_address: '127.0.0.1'
        })
      ).rejects.toThrow();
    });

    test('应该处理无效的任务标题', async () => {
      await expect(
        db.createTask({
          title: '',
          description: 'Desc',
          priority: 1,
          status: 'pending',
          assignee_id: null
        })
      ).rejects.toThrow();
    });
  });
});
