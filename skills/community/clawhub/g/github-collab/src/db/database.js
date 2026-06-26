/**
 * Database - 数据库操作类
 * 提供用户、Agent、任务的 CRUD 操作
 */

class Database {
  constructor(db) {
    this.db = db;
  }

  // ==================== 用户操作 ====================

  /**
   * 创建用户
   * @param {Object} userData - 用户数据
   * @param {string} userData.username - 用户名
   * @param {string} userData.email - 邮箱
   * @param {string} userData.password - 密码
   * @param {string} userData.role - 角色
   * @param {string} userData.status - 状态
   * @returns {Promise<Object>} 创建的用户
   */
  async createUser(userData) {
    const { username, email, password, role, status } = userData;

    // 验证输入
    if (!username || username.trim() === '') {
      throw new Error('用户名不能为空');
    }
    if (!email || !this.isValidEmail(email)) {
      throw new Error('无效的邮箱地址');
    }

    const now = new Date().toISOString();
    const result = await this.db.prepare(`
      INSERT INTO users (username, email, password, role, status, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `).run(username, email, password, role, status, now, now);

    const user = await this.getUser(result.lastInsertRowid);
    return user;
  }

  /**
   * 获取所有用户
   * @returns {Promise<Array>} 用户列表
   */
  async getUsers() {
    const rows = await this.db.prepare('SELECT * FROM users').all();
    return rows;
  }

  /**
   * 根据 ID 获取用户
   * @param {number} id - 用户 ID
   * @returns {Promise<Object|null>} 用户对象
   */
  async getUser(id) {
    const row = await this.db.prepare('SELECT * FROM users WHERE id = ?').get(id);
    return row || null;
  }

  /**
   * 更新用户
   * @param {number} id - 用户 ID
   * @param {Object} updates - 更新的数据
   * @returns {Promise<Object>} 更新结果 { changes: number }
   */
  async updateUser(id, updates) {
    const allowedFields = ['username', 'email', 'password', 'role', 'status'];
    const fields = Object.keys(updates).filter(f => allowedFields.includes(f));
    
    if (fields.length === 0) {
      return { changes: 0 };
    }

    const setClause = fields.map(f => `${f} = ?`).join(', ');
    const now = new Date().toISOString();
    const values = [...fields.map(f => updates[f]), now, id];

    const result = await this.db.prepare(`
      UPDATE users SET ${setClause}, updated_at = ?
      WHERE id = ?
    `).run(...values);

    return { changes: result.changes };
  }

  /**
   * 删除用户
   * @param {number} id - 用户 ID
   * @returns {Promise<Object>} 删除结果
   */
  async deleteUser(id) {
    const result = await this.db.prepare('DELETE FROM users WHERE id = ?').run(id);
    return { changes: result.changes };
  }

  /**
   * 根据邮箱获取用户
   * @param {string} email - 邮箱
   * @returns {Promise<Object|null>} 用户对象
   */
  async getUserByEmail(email) {
    const row = await this.db.prepare('SELECT * FROM users WHERE email = ?').get(email);
    return row || null;
  }

  /**
   * 根据用户名获取用户
   * @param {string} username - 用户名
   * @returns {Promise<Object|null>} 用户对象
   */
  async getUserByUsername(username) {
    const row = await this.db.prepare('SELECT * FROM users WHERE username = ?').get(username);
    return row || null;
  }

  /**
   * 更新用户密码
   * @param {number} id - 用户 ID
   * @param {string} newPassword - 新密码
   * @returns {Promise<Object>} 更新后的用户
   */
  async updateUserPassword(id, newPassword) {
    return this.updateUser(id, { password: newPassword });
  }

  /**
   * 更新用户状态
   * @param {number} id - 用户 ID
   * @param {string} status - 新状态
   * @returns {Promise<Object>} 更新后的用户
   */
  async updateUserStatus(id, status) {
    return this.updateUser(id, { status });
  }

  // ==================== Agent 操作 ====================

  /**
   * 创建 Agent
   * @param {Object} agentData - Agent 数据
   * @param {string} agentData.name - Agent 名称
   * @param {string} agentData.status - 状态
   * @param {number|null} agentData.current_task_id - 当前任务 ID
   * @param {string} agentData.last_heartbeat - 最后心跳时间
   * @param {string} agentData.ip_address - IP 地址
   * @returns {Promise<Object>} 创建的 Agent
   */
  async createAgent(agentData) {
    const { name, status, current_task_id, last_heartbeat, ip_address } = agentData;

    // 验证输入
    if (!name || name.trim() === '') {
      throw new Error('Agent 名称不能为空');
    }

    const now = new Date().toISOString();
    const result = await this.db.prepare(`
      INSERT INTO agents (name, status, current_task_id, last_heartbeat, ip_address, created_at)
      VALUES (?, ?, ?, ?, ?, ?)
    `).run(name, status, current_task_id, last_heartbeat, ip_address, now);

    const agent = await this.getAgent(result.lastInsertRowid);
    return agent;
  }

  /**
   * 获取所有 Agent
   * @returns {Promise<Array>} Agent 列表
   */
  async getAgents() {
    const rows = await this.db.prepare('SELECT * FROM agents').all();
    return rows;
  }

  /**
   * 根据 ID 获取 Agent
   * @param {number} id - Agent ID
   * @returns {Promise<Object|null>} Agent 对象
   */
  async getAgent(id) {
    const row = await this.db.prepare('SELECT * FROM agents WHERE id = ?').get(id);
    return row || null;
  }

  /**
   * 更新 Agent 状态
   * @param {number} id - Agent ID
   * @param {string} status - 新状态
   * @returns {Promise<Object>} 更新后的 Agent
   */
  async updateAgentStatus(id, status) {
    await this.db.prepare('UPDATE agents SET status = ?, updated_at = datetime("now") WHERE id = ?').run(status, id);
    return this.getAgent(id);
  }

  /**
   * 删除 Agent
   * @param {number} id - Agent ID
   * @returns {Promise<Object>} 删除结果
   */
  async deleteAgent(id) {
    const result = await this.db.prepare('DELETE FROM agents WHERE id = ?').run(id);
    return { changes: result.changes };
  }

  /**
   * 更新 Agent 心跳
   * @param {number} id - Agent ID
   * @param {string} heartbeatTime - 心跳时间
   * @returns {Promise<Object>} 更新后的 Agent
   */
  async updateAgentHeartbeat(id, heartbeatTime) {
    await this.db.prepare('UPDATE agents SET last_heartbeat = ?, updated_at = datetime("now") WHERE id = ?').run(heartbeatTime, id);
    return this.getAgent(id);
  }

  /**
   * 更新 Agent 当前任务
   * @param {number} id - Agent ID
   * @param {number} taskId - 任务 ID
   * @returns {Promise<Object>} 更新后的 Agent
   */
  async updateAgentCurrentTask(id, taskId) {
    const now = new Date().toISOString();
    await this.db.prepare("UPDATE agents SET current_task_id = ?, status = 'busy', updated_at = ? WHERE id = ?").run(taskId, now, id);
    return this.getAgent(id);
  }

  /**
   * 获取空闲 Agent
   * @returns {Promise<Array>} 空闲 Agent 列表
   */
  async getIdleAgents() {
    const rows = await this.db.prepare("SELECT * FROM agents WHERE status = 'idle'").all();
    return rows;
  }

  // ==================== 任务操作 ====================

  /**
   * 创建任务
   * @param {Object} taskData - 任务数据
   * @param {string} taskData.title - 任务标题
   * @param {string} taskData.description - 任务描述
   * @param {number} taskData.priority - 优先级
   * @param {string} taskData.status - 状态
   * @param {number|null} taskData.assignee_id - 分配给的用户 ID
   * @returns {Promise<Object>} 创建的任务
   */
  async createTask(taskData) {
    const { title, description, priority, status, assignee_id } = taskData;

    // 验证输入
    if (!title || title.trim() === '') {
      throw new Error('任务标题不能为空');
    }

    const now = new Date().toISOString();
    const result = await this.db.prepare(`
      INSERT INTO tasks (title, description, priority, status, assignee_id, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `).run(title, description, priority, status, assignee_id, now, now);

    const task = await this.getTask(result.lastInsertRowid);
    return task;
  }

  /**
   * 获取所有任务
   * @returns {Promise<Array>} 任务列表
   */
  async getTasks() {
    const rows = await this.db.prepare('SELECT * FROM tasks').all();
    return rows;
  }

  /**
   * 根据 ID 获取任务
   * @param {number} id - 任务 ID
   * @returns {Promise<Object|null>} 任务对象
   */
  async getTask(id) {
    const row = await this.db.prepare('SELECT * FROM tasks WHERE id = ?').get(id);
    return row || null;
  }

  /**
   * 更新任务状态
   * @param {number} id - 任务 ID
   * @param {string} status - 新状态
   * @returns {Promise<Object>} 更新后的任务
   */
  async updateTaskStatus(id, status) {
    await this.db.prepare('UPDATE tasks SET status = ?, updated_at = datetime("now") WHERE id = ?').run(status, id);
    return this.getTask(id);
  }

  /**
   * 删除任务
   * @param {number} id - 任务 ID
   * @returns {Promise<Object>} 删除结果
   */
  async deleteTask(id) {
    const result = await this.db.prepare('DELETE FROM tasks WHERE id = ?').run(id);
    return { changes: result.changes };
  }

  /**
   * 获取 Agent 的任务
   * @param {number} agentId - Agent ID
   * @returns {Promise<Array>} 任务列表
   */
  async getAgentTasks(agentId) {
    const rows = await this.db.prepare('SELECT * FROM tasks WHERE assignee_id = ?').all(agentId);
    return rows;
  }

  /**
   * 获取待分配任务
   * @returns {Promise<Array>} 待分配任务列表
   */
  async getPendingTasks() {
    const stmt = this.db.prepare("SELECT * FROM tasks WHERE status = 'pending' AND assignee_id IS NULL");
    const rows = await stmt.all();
    return rows;
  }

  /**
   * 分配任务给 Agent
   * @param {number} taskId - 任务 ID
   * @param {number} agentId - Agent ID
   * @returns {Promise<Object>} 更新后的任务
   */
  async assignTask(taskId, agentId) {
    const now = new Date().toISOString();
    await this.db.prepare(`
      UPDATE tasks SET assignee_id = ?, status = 'in_progress', updated_at = ?
      WHERE id = ?
    `).run(agentId, now, taskId);
    return this.getTask(taskId);
  }

  /**
   * 获取任务统计
   * @returns {Promise<Object>} 任务统计
   */
  async getTaskStats() {
    const total = await this.db.prepare('SELECT COUNT(*) as count FROM tasks').get();
    const pending = await this.db.prepare("SELECT COUNT(*) as count FROM tasks WHERE status = 'pending'").get();
    const inProgress = await this.db.prepare("SELECT COUNT(*) as count FROM tasks WHERE status = 'in_progress'").get();
    const completed = await this.db.prepare("SELECT COUNT(*) as count FROM tasks WHERE status = 'completed'").get();

    return {
      total: total?.count ?? 0,
      pending: pending?.count ?? 0,
      in_progress: inProgress?.count ?? 0,
      completed: completed?.count ?? 0
    };
  }

  // ==================== 工具方法 ====================

  /**
   * 验证邮箱格式
   * @param {string} email - 邮箱地址
   * @returns {boolean} 是否有效
   */
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  /**
   * 关闭数据库连接
   */
  async close() {
    if (this.db.close) {
      await this.db.close();
    }
  }
}

module.exports = { Database };