// src/build/standalone.ts
import Database from "better-sqlite3";
import path2 from "path";
import fs2 from "fs";

// src/utils/money.ts
function toCents(amount) {
  const normalized = formatMoney(amount);
  const [whole, frac] = normalized.replace("-", "").split(".");
  const cents = parseInt(whole, 10) * 100 + parseInt(frac, 10);
  return normalized.startsWith("-") ? -cents : cents;
}
function fromCents(cents) {
  const negative = cents < 0;
  const absCents = Math.abs(cents);
  const whole = Math.floor(absCents / 100);
  const frac = absCents % 100;
  const result = `${whole}.${frac.toString().padStart(2, "0")}`;
  return negative ? `-${result}` : result;
}
function formatMoney(amount) {
  const num = parseFloat(amount);
  if (isNaN(num)) return "0.00";
  return num.toFixed(2);
}
function moneyAdd(a, b) {
  return fromCents(toCents(a) + toCents(b));
}
function moneySubtract(a, b) {
  return fromCents(toCents(a) - toCents(b));
}
function isPositiveMoney(amount) {
  return toCents(amount) > 0;
}

// src/services/account.service.ts
var AccountService = class {
  constructor(db) {
    this.db = db;
  }
  db;
  list(includeArchived = false) {
    const sql = includeArchived ? "SELECT * FROM accounts ORDER BY sort_order, id" : "SELECT * FROM accounts WHERE is_archived = 0 ORDER BY sort_order, id";
    return this.db.prepare(sql).all();
  }
  getById(id) {
    const row = this.db.prepare("SELECT * FROM accounts WHERE id = ?").get(id);
    if (!row) throw new Error(`\u8D26\u6237 ID ${id} \u4E0D\u5B58\u5728`);
    return row;
  }
  add(input) {
    const existing = this.db.prepare("SELECT id FROM accounts WHERE name = ?").get(input.name);
    if (existing) throw new Error(`\u8D26\u6237\u540D "${input.name}" \u5DF2\u5B58\u5728`);
    const balance = formatMoney(input.initialBalance ?? "0.00");
    const stmt = this.db.prepare(`
      INSERT INTO accounts (name, type, icon, initial_balance, balance, remark)
      VALUES (@name, @type, @icon, @initialBalance, @balance, @remark)
    `);
    const info = stmt.run({
      name: input.name,
      type: input.type,
      icon: input.icon ?? "",
      initialBalance: balance,
      balance,
      remark: input.remark ?? ""
    });
    return this.getById(Number(info.lastInsertRowid));
  }
  update(input) {
    const account = this.getById(input.id);
    const fields = [];
    const params = { id: input.id };
    if (input.name !== void 0) {
      const dup = this.db.prepare("SELECT id FROM accounts WHERE name = ? AND id != ?").get(input.name, input.id);
      if (dup) throw new Error(`\u8D26\u6237\u540D "${input.name}" \u5DF2\u5B58\u5728`);
      fields.push("name = @name");
      params.name = input.name;
    }
    if (input.type !== void 0) {
      fields.push("type = @type");
      params.type = input.type;
    }
    if (input.icon !== void 0) {
      fields.push("icon = @icon");
      params.icon = input.icon;
    }
    if (input.remark !== void 0) {
      fields.push("remark = @remark");
      params.remark = input.remark;
    }
    if (input.sortOrder !== void 0) {
      fields.push("sort_order = @sortOrder");
      params.sortOrder = input.sortOrder;
    }
    if (fields.length === 0) return account;
    fields.push("updated_at = datetime('now','localtime')");
    this.db.prepare(`UPDATE accounts SET ${fields.join(", ")} WHERE id = @id`).run(params);
    return this.getById(input.id);
  }
  archive(id) {
    this.getById(id);
    this.db.prepare("UPDATE accounts SET is_archived = 1, updated_at = datetime('now','localtime') WHERE id = ?").run(id);
  }
  updateBalance(id, newBalance) {
    this.db.prepare("UPDATE accounts SET balance = ?, updated_at = datetime('now','localtime') WHERE id = ?").run(newBalance, id);
  }
};

// src/services/category.service.ts
var CategoryService = class {
  constructor(db) {
    this.db = db;
  }
  db;
  list(direction, includeArchived = false) {
    let sql = "SELECT * FROM categories";
    const conditions = [];
    const params = {};
    if (!includeArchived) {
      conditions.push("is_archived = 0");
    }
    if (direction) {
      conditions.push("direction = @direction");
      params.direction = direction;
    }
    if (conditions.length > 0) {
      sql += " WHERE " + conditions.join(" AND ");
    }
    sql += " ORDER BY sort_order, id";
    return this.db.prepare(sql).all(params);
  }
  getById(id) {
    const row = this.db.prepare("SELECT * FROM categories WHERE id = ?").get(id);
    if (!row) throw new Error(`\u5206\u7C7B ID ${id} \u4E0D\u5B58\u5728`);
    return row;
  }
  add(input) {
    const parentId = input.parentId ?? 0;
    const existing = this.db.prepare(
      "SELECT id FROM categories WHERE name = ? AND direction = ? AND parent_id = ?"
    ).get(input.name, input.direction, parentId);
    if (existing) throw new Error(`\u5206\u7C7B "${input.name}" (${input.direction}) \u5DF2\u5B58\u5728`);
    const info = this.db.prepare(`
      INSERT INTO categories (name, direction, parent_id, icon)
      VALUES (@name, @direction, @parentId, @icon)
    `).run({
      name: input.name,
      direction: input.direction,
      parentId,
      icon: input.icon ?? ""
    });
    return this.getById(Number(info.lastInsertRowid));
  }
  update(input) {
    const category = this.getById(input.id);
    const fields = [];
    const params = { id: input.id };
    if (input.name !== void 0) {
      const dup = this.db.prepare(
        "SELECT id FROM categories WHERE name = ? AND direction = ? AND parent_id = ? AND id != ?"
      ).get(input.name, category.direction, category.parent_id, input.id);
      if (dup) throw new Error(`\u5206\u7C7B "${input.name}" \u5DF2\u5B58\u5728`);
      fields.push("name = @name");
      params.name = input.name;
    }
    if (input.icon !== void 0) {
      fields.push("icon = @icon");
      params.icon = input.icon;
    }
    if (input.sortOrder !== void 0) {
      fields.push("sort_order = @sortOrder");
      params.sortOrder = input.sortOrder;
    }
    if (fields.length === 0) return category;
    fields.push("updated_at = datetime('now','localtime')");
    this.db.prepare(`UPDATE categories SET ${fields.join(", ")} WHERE id = @id`).run(params);
    return this.getById(input.id);
  }
  archive(id) {
    this.getById(id);
    const children = this.db.prepare("SELECT id FROM categories WHERE parent_id = ? AND is_archived = 0").all(id);
    if (children.length > 0) throw new Error("\u5B58\u5728\u5B50\u5206\u7C7B\uFF0C\u65E0\u6CD5\u5F52\u6863");
    this.db.prepare("UPDATE categories SET is_archived = 1, updated_at = datetime('now','localtime') WHERE id = ?").run(id);
  }
  getTree(direction) {
    const all = this.list(direction);
    all.forEach((c) => c.children = []);
    const map = /* @__PURE__ */ new Map();
    all.forEach((c) => map.set(c.id, c));
    const roots = [];
    all.forEach((c) => {
      if (c.parent_id === 0 || !map.has(c.parent_id)) {
        roots.push(c);
      } else {
        map.get(c.parent_id).children.push(c);
      }
    });
    return roots;
  }
};

// src/utils/date.ts
function formatDateTime(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  const h = String(date.getHours()).padStart(2, "0");
  const min = String(date.getMinutes()).padStart(2, "0");
  const s = String(date.getSeconds()).padStart(2, "0");
  return `${y}-${m}-${d} ${h}:${min}:${s}`;
}
function getCurrentDateTime() {
  return formatDateTime(/* @__PURE__ */ new Date());
}
function getMonthRange(year, month) {
  const lastDay = new Date(year, month, 0).getDate();
  return {
    start: `${year}-${String(month).padStart(2, "0")}-01 00:00:00`,
    end: `${year}-${String(month).padStart(2, "0")}-${String(lastDay).padStart(2, "0")} 23:59:59`
  };
}
function getYearRange(year) {
  return {
    start: `${year}-01-01 00:00:00`,
    end: `${year}-12-31 23:59:59`
  };
}

// src/services/transaction.service.ts
var TransactionService = class {
  constructor(db) {
    this.db = db;
  }
  db;
  add(input) {
    this.validateAdd(input);
    const happenTime = input.happenTime ?? getCurrentDateTime();
    const amount = formatMoney(input.amount);
    const insert = this.db.transaction(() => {
      const info = this.db.prepare(`
        INSERT INTO transactions (type, amount, account_id, to_account_id, category_id, remark, happen_time)
        VALUES (@type, @amount, @accountId, @toAccountId, @categoryId, @remark, @happenTime)
      `).run({
        type: input.type,
        amount,
        accountId: input.accountId,
        toAccountId: input.toAccountId ?? null,
        categoryId: input.categoryId ?? null,
        remark: input.remark ?? "",
        happenTime
      });
      this.applyBalance(input.type, amount, input.accountId, input.toAccountId);
      return Number(info.lastInsertRowid);
    });
    const id = insert();
    return this.getById(id);
  }
  getById(id) {
    const row = this.db.prepare("SELECT * FROM transactions WHERE id = ? AND is_deleted = 0").get(id);
    if (!row) throw new Error(`\u4EA4\u6613 ID ${id} \u4E0D\u5B58\u5728`);
    return row;
  }
  list(input) {
    const conditions = ["is_deleted = 0"];
    const params = {};
    if (input.startDate) {
      conditions.push("happen_time >= @startDate");
      params.startDate = input.startDate + (input.startDate.includes(" ") ? "" : " 00:00:00");
    }
    if (input.endDate) {
      conditions.push("happen_time <= @endDate");
      params.endDate = input.endDate + (input.endDate.includes(" ") ? "" : " 23:59:59");
    }
    if (!input.startDate && !input.endDate) {
      const now = /* @__PURE__ */ new Date();
      const range = getMonthRange(now.getFullYear(), now.getMonth() + 1);
      conditions.push("happen_time >= @startDate");
      conditions.push("happen_time <= @endDate");
      params.startDate = range.start;
      params.endDate = range.end;
    }
    if (input.type) {
      conditions.push("type = @type");
      params.type = input.type;
    }
    if (input.accountId) {
      conditions.push("(account_id = @accountId OR to_account_id = @accountId)");
      params.accountId = input.accountId;
    }
    if (input.categoryId) {
      conditions.push("category_id = @categoryId");
      params.categoryId = input.categoryId;
    }
    if (input.keyword) {
      conditions.push("remark LIKE @keyword");
      params.keyword = `%${input.keyword}%`;
    }
    const limit = input.limit ?? 20;
    const offset = input.offset ?? 0;
    const sql = `SELECT * FROM transactions WHERE ${conditions.join(" AND ")} ORDER BY happen_time DESC LIMIT ${limit} OFFSET ${offset}`;
    return this.db.prepare(sql).all(params);
  }
  update(input) {
    const old = this.getById(input.id);
    const doUpdate = this.db.transaction(() => {
      this.rollbackBalance(old.type, old.amount, old.account_id, old.to_account_id);
      const fields = [];
      const params = { id: input.id };
      const newType = input.type ?? old.type;
      const newAmount = input.amount ? formatMoney(input.amount) : old.amount;
      const newAccountId = input.accountId ?? old.account_id;
      const newToAccountId = input.toAccountId ?? old.to_account_id;
      const newCategoryId = input.categoryId !== void 0 ? input.categoryId : old.category_id;
      this.validateUpdate(newType, newCategoryId, newAccountId, newToAccountId);
      if (input.type !== void 0) {
        fields.push("type = @type");
        params.type = input.type;
      }
      if (input.amount !== void 0) {
        fields.push("amount = @amount");
        params.amount = newAmount;
      }
      if (input.accountId !== void 0) {
        fields.push("account_id = @accountId");
        params.accountId = input.accountId;
      }
      if (input.toAccountId !== void 0) {
        fields.push("to_account_id = @toAccountId");
        params.toAccountId = input.toAccountId;
      }
      if (input.categoryId !== void 0) {
        fields.push("category_id = @categoryId");
        params.categoryId = input.categoryId;
      }
      if (input.remark !== void 0) {
        fields.push("remark = @remark");
        params.remark = input.remark;
      }
      if (input.happenTime !== void 0) {
        fields.push("happen_time = @happenTime");
        params.happenTime = input.happenTime;
      }
      if (fields.length > 0) {
        fields.push("updated_at = datetime('now','localtime')");
        this.db.prepare(`UPDATE transactions SET ${fields.join(", ")} WHERE id = @id`).run(params);
      }
      this.applyBalance(newType, newAmount, newAccountId, newToAccountId ?? void 0);
    });
    doUpdate();
    return this.getById(input.id);
  }
  delete(id) {
    const tx = this.getById(id);
    const doDelete = this.db.transaction(() => {
      this.db.prepare("UPDATE transactions SET is_deleted = 1, updated_at = datetime('now','localtime') WHERE id = ?").run(id);
      this.rollbackBalance(tx.type, tx.amount, tx.account_id, tx.to_account_id);
    });
    doDelete();
  }
  applyBalance(type, amount, accountId, toAccountId) {
    const account = this.db.prepare("SELECT balance FROM accounts WHERE id = ?").get(accountId);
    if (type === "INCOME") {
      this.db.prepare("UPDATE accounts SET balance = ?, updated_at = datetime('now','localtime') WHERE id = ?").run(moneyAdd(account.balance, amount), accountId);
    } else if (type === "EXPENSE") {
      this.db.prepare("UPDATE accounts SET balance = ?, updated_at = datetime('now','localtime') WHERE id = ?").run(moneySubtract(account.balance, amount), accountId);
    } else if (type === "TRANSFER" && toAccountId) {
      const toAccount = this.db.prepare("SELECT balance FROM accounts WHERE id = ?").get(toAccountId);
      this.db.prepare("UPDATE accounts SET balance = ?, updated_at = datetime('now','localtime') WHERE id = ?").run(moneySubtract(account.balance, amount), accountId);
      this.db.prepare("UPDATE accounts SET balance = ?, updated_at = datetime('now','localtime') WHERE id = ?").run(moneyAdd(toAccount.balance, amount), toAccountId);
    }
  }
  rollbackBalance(type, amount, accountId, toAccountId) {
    const account = this.db.prepare("SELECT balance FROM accounts WHERE id = ?").get(accountId);
    if (type === "INCOME") {
      this.db.prepare("UPDATE accounts SET balance = ?, updated_at = datetime('now','localtime') WHERE id = ?").run(moneySubtract(account.balance, amount), accountId);
    } else if (type === "EXPENSE") {
      this.db.prepare("UPDATE accounts SET balance = ?, updated_at = datetime('now','localtime') WHERE id = ?").run(moneyAdd(account.balance, amount), accountId);
    } else if (type === "TRANSFER" && toAccountId) {
      const toAccount = this.db.prepare("SELECT balance FROM accounts WHERE id = ?").get(toAccountId);
      this.db.prepare("UPDATE accounts SET balance = ?, updated_at = datetime('now','localtime') WHERE id = ?").run(moneyAdd(account.balance, amount), accountId);
      this.db.prepare("UPDATE accounts SET balance = ?, updated_at = datetime('now','localtime') WHERE id = ?").run(moneySubtract(toAccount.balance, amount), toAccountId);
    }
  }
  validateUpdate(type, categoryId, accountId, toAccountId) {
    if (type === "TRANSFER") {
      if (!toAccountId) throw new Error("\u8F6C\u8D26\u5FC5\u987B\u63D0\u4F9B toAccountId");
      if (accountId === toAccountId) throw new Error("\u8F6C\u8D26\u6E90\u548C\u76EE\u6807\u8D26\u6237\u4E0D\u80FD\u76F8\u540C");
    } else {
      if (!categoryId) throw new Error(`${type} \u4EA4\u6613\u5FC5\u987B\u63D0\u4F9B categoryId`);
      const category = this.db.prepare("SELECT direction FROM categories WHERE id = ?").get(categoryId);
      if (!category) throw new Error(`\u5206\u7C7B ID ${categoryId} \u4E0D\u5B58\u5728`);
      const expectedDirection = type === "INCOME" ? "INCOME" : "EXPENSE";
      if (category.direction !== expectedDirection) {
        throw new Error(`\u5206\u7C7B\u65B9\u5411\u4E0D\u5339\u914D\uFF1A\u4EA4\u6613\u7C7B\u578B ${type} \u9700\u8981 ${expectedDirection} \u5206\u7C7B`);
      }
    }
  }
  validateAdd(input) {
    if (isNaN(parseFloat(input.amount))) {
      throw new Error("\u91D1\u989D\u683C\u5F0F\u65E0\u6548");
    }
    if (!isPositiveMoney(input.amount)) {
      throw new Error("\u91D1\u989D\u5FC5\u987B\u5927\u4E8E 0");
    }
    const account = this.db.prepare("SELECT id FROM accounts WHERE id = ?").get(input.accountId);
    if (!account) throw new Error(`\u8D26\u6237 ID ${input.accountId} \u4E0D\u5B58\u5728`);
    if (input.type === "TRANSFER") {
      if (!input.toAccountId) throw new Error("\u8F6C\u8D26\u5FC5\u987B\u63D0\u4F9B toAccountId");
      if (input.accountId === input.toAccountId) throw new Error("\u8F6C\u8D26\u6E90\u548C\u76EE\u6807\u8D26\u6237\u4E0D\u80FD\u76F8\u540C");
      const toAccount = this.db.prepare("SELECT id FROM accounts WHERE id = ?").get(input.toAccountId);
      if (!toAccount) throw new Error(`\u76EE\u6807\u8D26\u6237 ID ${input.toAccountId} \u4E0D\u5B58\u5728`);
    } else {
      if (!input.categoryId) throw new Error(`${input.type} \u4EA4\u6613\u5FC5\u987B\u63D0\u4F9B categoryId`);
      const category = this.db.prepare("SELECT direction FROM categories WHERE id = ?").get(input.categoryId);
      if (!category) throw new Error(`\u5206\u7C7B ID ${input.categoryId} \u4E0D\u5B58\u5728`);
      const expectedDirection = input.type === "INCOME" ? "INCOME" : "EXPENSE";
      if (category.direction !== expectedDirection) {
        throw new Error(`\u5206\u7C7B\u65B9\u5411\u4E0D\u5339\u914D\uFF1A\u4EA4\u6613\u7C7B\u578B ${input.type} \u9700\u8981 ${expectedDirection} \u5206\u7C7B`);
      }
    }
  }
};

// src/services/budget.service.ts
var BudgetService = class {
  constructor(db) {
    this.db = db;
  }
  db;
  set(input) {
    const amount = formatMoney(input.amount);
    const categoryId = input.categoryId ?? null;
    const month = input.month ?? null;
    const existing = this.db.prepare(
      "SELECT id FROM budgets WHERE category_id IS @categoryId AND period_type = @periodType AND year = @year AND month IS @month"
    ).get({ categoryId, periodType: input.periodType, year: input.year, month });
    if (existing) {
      this.db.prepare("UPDATE budgets SET amount = ?, remark = ?, updated_at = datetime('now','localtime') WHERE id = ?").run(amount, input.remark ?? "", existing.id);
      return this.getById(existing.id);
    }
    const info = this.db.prepare(`
      INSERT INTO budgets (category_id, amount, period_type, year, month, remark)
      VALUES (@categoryId, @amount, @periodType, @year, @month, @remark)
    `).run({
      categoryId,
      amount,
      periodType: input.periodType,
      year: input.year,
      month,
      remark: input.remark ?? ""
    });
    return this.getById(Number(info.lastInsertRowid));
  }
  getById(id) {
    const row = this.db.prepare("SELECT * FROM budgets WHERE id = ?").get(id);
    if (!row) throw new Error(`\u9884\u7B97 ID ${id} \u4E0D\u5B58\u5728`);
    return row;
  }
  list(year, month) {
    if (month) {
      return this.db.prepare("SELECT * FROM budgets WHERE year = ? AND (month = ? OR month IS NULL) AND period_type = ?").all(year, month, "MONTHLY");
    }
    return this.db.prepare("SELECT * FROM budgets WHERE year = ?").all(year);
  }
  delete(id) {
    this.getById(id);
    this.db.prepare("DELETE FROM budgets WHERE id = ?").run(id);
  }
  getStatus(input) {
    const budgets = input.categoryId ? this.db.prepare("SELECT * FROM budgets WHERE year = @year AND month IS @month AND category_id = @catId").all({ year: input.year, month: input.month ?? null, catId: input.categoryId }) : this.list(input.year, input.month);
    const range = input.month ? getMonthRange(input.year, input.month) : getYearRange(input.year);
    return budgets.map((budget) => {
      let spentSql;
      let spentParams;
      if (budget.category_id) {
        spentSql = `SELECT COALESCE(SUM(CAST(amount AS REAL)), 0) as total
                     FROM transactions
                     WHERE type = 'EXPENSE' AND is_deleted = 0
                       AND category_id = @categoryId
                       AND happen_time >= @start AND happen_time <= @end`;
        spentParams = { categoryId: budget.category_id, start: range.start, end: range.end };
      } else {
        spentSql = `SELECT COALESCE(SUM(CAST(amount AS REAL)), 0) as total
                     FROM transactions
                     WHERE type = 'EXPENSE' AND is_deleted = 0
                       AND happen_time >= @start AND happen_time <= @end`;
        spentParams = { start: range.start, end: range.end };
      }
      const { total } = this.db.prepare(spentSql).get(spentParams);
      const spent = formatMoney(total.toString());
      const remaining = moneySubtract(budget.amount, spent);
      const percentUsed = parseFloat(budget.amount) === 0 ? 0 : Math.round(total * 100 / parseFloat(budget.amount));
      let categoryName = null;
      if (budget.category_id) {
        const cat = this.db.prepare("SELECT name FROM categories WHERE id = ?").get(budget.category_id);
        categoryName = cat?.name ?? null;
      }
      return {
        budgetId: budget.id,
        categoryId: budget.category_id,
        categoryName,
        budgetAmount: budget.amount,
        spent,
        remaining,
        percentUsed
      };
    });
  }
};

// src/services/report.service.ts
var ReportService = class {
  constructor(db) {
    this.db = db;
  }
  db;
  monthlySummary(year, month) {
    const range = getMonthRange(year, month);
    return this.summaryForRange(year, month, range.start, range.end);
  }
  yearlySummary(year) {
    const range = getYearRange(year);
    const overall = this.summaryForRange(year, 0, range.start, range.end);
    const months = [];
    for (let m = 1; m <= 12; m++) {
      months.push(this.monthlySummary(year, m));
    }
    return {
      year,
      totalIncome: overall.totalIncome,
      totalExpense: overall.totalExpense,
      netBalance: overall.netBalance,
      months
    };
  }
  categoryBreakdown(year, month, direction) {
    const range = month ? getMonthRange(year, month) : getYearRange(year);
    const dir = direction ?? "EXPENSE";
    const rows = this.db.prepare(`
      SELECT c.id as categoryId, c.name as categoryName,
             COALESCE(SUM(CAST(t.amount AS REAL)), 0) as total,
             COUNT(t.id) as count
      FROM transactions t
      JOIN categories c ON t.category_id = c.id
      WHERE t.is_deleted = 0 AND t.type = @dir
        AND t.happen_time >= @start AND t.happen_time <= @end
      GROUP BY c.id, c.name
      ORDER BY total DESC
    `).all({ dir, start: range.start, end: range.end });
    const grandTotal = rows.reduce((sum, r) => sum + r.total, 0);
    return rows.map((r) => ({
      categoryId: r.categoryId,
      categoryName: r.categoryName,
      amount: formatMoney(r.total.toString()),
      percentage: grandTotal === 0 ? 0 : Math.round(r.total / grandTotal * 100),
      count: r.count
    }));
  }
  monthlyTrend(year) {
    const trend = [];
    for (let m = 1; m <= 12; m++) {
      const range = getMonthRange(year, m);
      const income = this.sumByType("INCOME", range.start, range.end);
      const expense = this.sumByType("EXPENSE", range.start, range.end);
      trend.push({
        month: m,
        income: formatMoney(income.toString()),
        expense: formatMoney(expense.toString()),
        net: moneySubtract(formatMoney(income.toString()), formatMoney(expense.toString()))
      });
    }
    return trend;
  }
  balanceOverview() {
    return this.db.prepare("SELECT * FROM accounts WHERE is_archived = 0 ORDER BY sort_order, id").all();
  }
  summaryForRange(year, month, start, end) {
    const income = this.sumByType("INCOME", start, end);
    const expense = this.sumByType("EXPENSE", start, end);
    const incomeCount = this.countByType("INCOME", start, end);
    const expenseCount = this.countByType("EXPENSE", start, end);
    return {
      year,
      month,
      totalIncome: formatMoney(income.toString()),
      totalExpense: formatMoney(expense.toString()),
      netBalance: moneySubtract(formatMoney(income.toString()), formatMoney(expense.toString())),
      incomeCount,
      expenseCount
    };
  }
  sumByType(type, start, end) {
    const row = this.db.prepare(
      `SELECT COALESCE(SUM(CAST(amount AS REAL)), 0) as total FROM transactions
       WHERE type = ? AND is_deleted = 0 AND happen_time >= ? AND happen_time <= ?`
    ).get(type, start, end);
    return row.total;
  }
  countByType(type, start, end) {
    const row = this.db.prepare(
      `SELECT COUNT(*) as count FROM transactions
       WHERE type = ? AND is_deleted = 0 AND happen_time >= ? AND happen_time <= ?`
    ).get(type, start, end);
    return row.count;
  }
};

// src/services/data.service.ts
import fs from "fs";
import path from "path";
var DataService = class {
  constructor(db) {
    this.db = db;
  }
  db;
  export(input) {
    const conditions = ["t.is_deleted = 0"];
    const params = {};
    if (input.startDate) {
      conditions.push("t.happen_time >= @startDate");
      params.startDate = input.startDate + (input.startDate.includes(" ") ? "" : " 00:00:00");
    }
    if (input.endDate) {
      conditions.push("t.happen_time <= @endDate");
      params.endDate = input.endDate + (input.endDate.includes(" ") ? "" : " 23:59:59");
    }
    const rows = this.db.prepare(`
      SELECT t.*, a.name as account_name, ta.name as to_account_name, c.name as category_name
      FROM transactions t
      LEFT JOIN accounts a ON t.account_id = a.id
      LEFT JOIN accounts ta ON t.to_account_id = ta.id
      LEFT JOIN categories c ON t.category_id = c.id
      WHERE ${conditions.join(" AND ")}
      ORDER BY t.happen_time DESC
    `).all(params);
    let content;
    if (input.format === "json") {
      content = JSON.stringify(rows, null, 2);
    } else {
      const header = "id,type,amount,account,to_account,category,remark,happen_time";
      const escapeCsv = (s) => s.replace(/"/g, '""');
      const lines = rows.map(
        (r) => `${r.id},${r.type},${r.amount},"${escapeCsv(r.account_name)}","${escapeCsv(r.to_account_name ?? "")}","${escapeCsv(r.category_name ?? "")}","${escapeCsv(r.remark)}","${r.happen_time}"`
      );
      content = [header, ...lines].join("\n");
    }
    const outputPath = input.outputPath ?? path.join(process.cwd(), `export_${Date.now()}.${input.format}`);
    fs.writeFileSync(outputPath, content, "utf-8");
    return outputPath;
  }
  import(input) {
    if (input.format !== "csv") {
      throw new Error(`\u6682\u4E0D\u652F\u6301 ${input.format} \u683C\u5F0F\u5BFC\u5165\uFF0C\u76EE\u524D\u4EC5\u652F\u6301 csv`);
    }
    const content = fs.readFileSync(input.file, "utf-8");
    const lines = content.split("\n").filter((l) => l.trim());
    if (lines.length < 2) return { imported: 0, skipped: 0 };
    const dataLines = lines.slice(1);
    let imported = 0;
    let skipped = 0;
    const categories = this.db.prepare("SELECT * FROM categories WHERE is_archived = 0").all();
    const accounts = this.db.prepare("SELECT * FROM accounts WHERE is_archived = 0").all();
    const findCategory = (name, direction) => {
      const cat = categories.find((c) => c.name === name && c.direction === direction);
      if (cat) return cat.id;
      const fallback = categories.find((c) => c.name === (direction === "INCOME" ? "\u5176\u4ED6\u6536\u5165" : "\u5176\u4ED6\u652F\u51FA"));
      return fallback?.id ?? null;
    };
    const findAccount = (name) => {
      const acc = accounts.find((a) => a.name === name);
      return acc?.id ?? null;
    };
    const insertTx = this.db.prepare(`
      INSERT INTO transactions (type, amount, account_id, to_account_id, category_id, remark, happen_time)
      VALUES (@type, @amount, @accountId, @toAccountId, @categoryId, @remark, @happenTime)
    `);
    const updateBalance = this.db.prepare(
      "UPDATE accounts SET balance = @balance, updated_at = datetime('now','localtime') WHERE id = @id"
    );
    const doImport = this.db.transaction(() => {
      for (const line of dataLines) {
        try {
          const parts = this.parseCsvLine(line);
          if (parts.length < 8) {
            skipped++;
            continue;
          }
          const [, type, amount, accountName, toAccountName, categoryName, remark, happenTime] = parts;
          const accountId = findAccount(accountName);
          if (!accountId) {
            skipped++;
            continue;
          }
          const toAccountId = toAccountName ? findAccount(toAccountName) : null;
          const categoryId = categoryName ? findCategory(categoryName, type === "INCOME" ? "INCOME" : "EXPENSE") : null;
          const formattedAmount = formatMoney(amount);
          insertTx.run({
            type,
            amount: formattedAmount,
            accountId,
            toAccountId,
            categoryId,
            remark: remark ?? "",
            happenTime: happenTime || getCurrentDateTime()
          });
          const acct = this.db.prepare("SELECT balance FROM accounts WHERE id = ?").get(accountId);
          if (type === "INCOME") {
            updateBalance.run({ balance: moneyAdd(acct.balance, formattedAmount), id: accountId });
          } else if (type === "EXPENSE") {
            updateBalance.run({ balance: moneySubtract(acct.balance, formattedAmount), id: accountId });
          } else if (type === "TRANSFER" && toAccountId) {
            updateBalance.run({ balance: moneySubtract(acct.balance, formattedAmount), id: accountId });
            const toAcct = this.db.prepare("SELECT balance FROM accounts WHERE id = ?").get(toAccountId);
            updateBalance.run({ balance: moneyAdd(toAcct.balance, formattedAmount), id: toAccountId });
          }
          imported++;
        } catch {
          skipped++;
        }
      }
    });
    doImport();
    return { imported, skipped };
  }
  parseCsvLine(line) {
    const result = [];
    let current = "";
    let inQuotes = false;
    for (const char of line) {
      if (char === '"') {
        inQuotes = !inQuotes;
      } else if (char === "," && !inQuotes) {
        result.push(current.trim());
        current = "";
      } else {
        current += char;
      }
    }
    result.push(current.trim());
    return result;
  }
};

// src/build/standalone.ts
var MIGRATION_001 = `
CREATE TABLE IF NOT EXISTS accounts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT    NOT NULL UNIQUE,
    type            TEXT    NOT NULL CHECK (type IN ('CASH','BANK','CREDIT','ALIPAY','WECHAT','OTHER')),
    icon            TEXT    DEFAULT '',
    initial_balance TEXT    NOT NULL DEFAULT '0.00',
    balance         TEXT    NOT NULL DEFAULT '0.00',
    currency        TEXT    NOT NULL DEFAULT 'CNY',
    sort_order      INTEGER NOT NULL DEFAULT 0,
    is_archived     INTEGER NOT NULL DEFAULT 0,
    remark          TEXT    DEFAULT '',
    created_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS categories (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT    NOT NULL,
    direction       TEXT    NOT NULL CHECK (direction IN ('INCOME','EXPENSE')),
    parent_id       INTEGER DEFAULT 0,
    icon            TEXT    DEFAULT '',
    sort_order      INTEGER NOT NULL DEFAULT 0,
    is_archived     INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
    UNIQUE(name, direction, parent_id)
);

CREATE TABLE IF NOT EXISTS transactions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    type            TEXT    NOT NULL CHECK (type IN ('INCOME','EXPENSE','TRANSFER')),
    amount          TEXT    NOT NULL,
    account_id      INTEGER NOT NULL REFERENCES accounts(id),
    to_account_id   INTEGER REFERENCES accounts(id),
    category_id     INTEGER REFERENCES categories(id),
    remark          TEXT    DEFAULT '',
    happen_time     TEXT    NOT NULL,
    is_deleted      INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE INDEX IF NOT EXISTS idx_transactions_happen_time ON transactions(happen_time);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);
CREATE INDEX IF NOT EXISTS idx_transactions_account_id ON transactions(account_id);
CREATE INDEX IF NOT EXISTS idx_transactions_category_id ON transactions(category_id);
CREATE INDEX IF NOT EXISTS idx_transactions_is_deleted ON transactions(is_deleted);

CREATE TABLE IF NOT EXISTS budgets (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id     INTEGER REFERENCES categories(id),
    amount          TEXT    NOT NULL,
    period_type     TEXT    NOT NULL CHECK (period_type IN ('MONTHLY','YEARLY')),
    year            INTEGER NOT NULL,
    month           INTEGER,
    remark          TEXT    DEFAULT '',
    created_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
    UNIQUE(category_id, period_type, year, month)
);

CREATE INDEX IF NOT EXISTS idx_budgets_period ON budgets(period_type, year, month);
`;
var MIGRATION_002 = `
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u9910\u996E', 'EXPENSE', 'food', 10);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u4EA4\u901A', 'EXPENSE', 'transport', 20);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u8D2D\u7269', 'EXPENSE', 'shopping', 30);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u4F4F\u623F', 'EXPENSE', 'housing', 40);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u5A31\u4E50', 'EXPENSE', 'entertainment', 50);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u533B\u7597', 'EXPENSE', 'medical', 60);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u5B66\u4E60', 'EXPENSE', 'education', 70);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u901A\u8BAF', 'EXPENSE', 'telecom', 80);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u65E5\u7528', 'EXPENSE', 'daily', 90);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u5176\u4ED6\u652F\u51FA', 'EXPENSE', 'other', 100);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u5DE5\u8D44', 'INCOME', 'salary', 10);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u5956\u91D1', 'INCOME', 'bonus', 20);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u6295\u8D44', 'INCOME', 'investment', 30);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u9000\u6B3E', 'INCOME', 'refund', 40);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u517C\u804C', 'INCOME', 'part_time', 50);
INSERT OR IGNORE INTO categories (name, direction, icon, sort_order) VALUES ('\u5176\u4ED6\u6536\u5165', 'INCOME', 'other', 60);
INSERT OR IGNORE INTO accounts (name, type, icon, initial_balance, balance, sort_order) VALUES ('\u73B0\u91D1', 'CASH', 'cash', '0.00', '0.00', 10);
INSERT OR IGNORE INTO accounts (name, type, icon, initial_balance, balance, sort_order) VALUES ('\u652F\u4ED8\u5B9D', 'ALIPAY', 'alipay', '0.00', '0.00', 20);
INSERT OR IGNORE INTO accounts (name, type, icon, initial_balance, balance, sort_order) VALUES ('\u5FAE\u4FE1', 'WECHAT', 'wechat', '0.00', '0.00', 30);
`;
var MIGRATIONS = [
  { filename: "001_create_tables.sql", sql: MIGRATION_001 },
  { filename: "002_seed_defaults.sql", sql: MIGRATION_002 }
];
function runMigrations(db) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS _migrations (
      id        INTEGER PRIMARY KEY AUTOINCREMENT,
      filename  TEXT NOT NULL UNIQUE,
      applied_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
    )
  `);
  const applied = new Set(
    db.prepare("SELECT filename FROM _migrations").all().map((r) => r.filename)
  );
  const insertMigration = db.prepare("INSERT INTO _migrations (filename) VALUES (?)");
  for (const { filename, sql } of MIGRATIONS) {
    if (applied.has(filename)) continue;
    const migrate = db.transaction(() => {
      db.exec(sql);
      insertMigration.run(filename);
    });
    migrate();
  }
}
function getDb() {
  const dbPath = process.env.LYUUO_BOOK_DB_PATH || path2.join(process.env.HOME || process.env.USERPROFILE || ".", ".lyuuo-book", "data", "book.db");
  const dir = path2.dirname(dbPath);
  if (!fs2.existsSync(dir)) {
    fs2.mkdirSync(dir, { recursive: true });
  }
  const db = new Database(dbPath);
  db.pragma("journal_mode = WAL");
  db.pragma("foreign_keys = ON");
  runMigrations(db);
  return db;
}
function parseCommand(args) {
  if (args.length === 0) throw new Error("\u7F3A\u5C11\u547D\u4EE4\u3002\u7528\u6CD5: node book.mjs <command> [json_params]");
  const command = args[0];
  if (!args[1]) return { command, params: {} };
  try {
    const params = JSON.parse(args[1]);
    return { command, params };
  } catch {
    throw new Error(`JSON \u53C2\u6570\u683C\u5F0F\u9519\u8BEF: "${args[1]}" \u4E0D\u662F\u6709\u6548\u7684 JSON`);
  }
}
function main() {
  const args = process.argv.slice(2);
  let result;
  try {
    const { command, params } = parseCommand(args);
    const db = getDb();
    const accountService = new AccountService(db);
    const categoryService = new CategoryService(db);
    const txService = new TransactionService(db);
    const budgetService = new BudgetService(db);
    const reportService = new ReportService(db);
    const dataService = new DataService(db);
    const p = params;
    switch (command) {
      case "account:add":
        result = { success: true, data: accountService.add(p) };
        break;
      case "account:list":
        result = { success: true, data: accountService.list(p.includeArchived ?? false) };
        break;
      case "account:update":
        result = { success: true, data: accountService.update(p) };
        break;
      case "account:archive":
        accountService.archive(p.id);
        result = { success: true, data: { message: "\u5DF2\u5F52\u6863" } };
        break;
      case "category:add":
        result = { success: true, data: categoryService.add(p) };
        break;
      case "category:list":
        result = { success: true, data: p.tree ? categoryService.getTree(p.direction) : categoryService.list(p.direction, p.includeArchived) };
        break;
      case "category:update":
        result = { success: true, data: categoryService.update(p) };
        break;
      case "category:archive":
        categoryService.archive(p.id);
        result = { success: true, data: { message: "\u5DF2\u5F52\u6863" } };
        break;
      case "transaction:add":
        result = { success: true, data: txService.add(p) };
        break;
      case "transaction:list":
        result = { success: true, data: txService.list(p) };
        break;
      case "transaction:get":
        result = { success: true, data: txService.getById(p.id) };
        break;
      case "transaction:update":
        result = { success: true, data: txService.update(p) };
        break;
      case "transaction:delete":
        txService.delete(p.id);
        result = { success: true, data: { message: "\u5DF2\u5220\u9664" } };
        break;
      case "budget:set":
        result = { success: true, data: budgetService.set(p) };
        break;
      case "budget:list":
        result = { success: true, data: budgetService.list(p.year, p.month) };
        break;
      case "budget:status":
        result = { success: true, data: budgetService.getStatus(p) };
        break;
      case "budget:delete":
        budgetService.delete(p.id);
        result = { success: true, data: { message: "\u5DF2\u5220\u9664" } };
        break;
      case "report:monthly":
        result = { success: true, data: reportService.monthlySummary(p.year, p.month) };
        break;
      case "report:yearly":
        result = { success: true, data: reportService.yearlySummary(p.year) };
        break;
      case "report:category":
        result = { success: true, data: reportService.categoryBreakdown(p.year, p.month, p.direction) };
        break;
      case "report:trend":
        result = { success: true, data: reportService.monthlyTrend(p.year) };
        break;
      case "report:balance":
        result = { success: true, data: reportService.balanceOverview() };
        break;
      case "data:export":
        result = { success: true, data: { path: dataService.export(p) } };
        break;
      case "data:import":
        result = { success: true, data: dataService.import(p) };
        break;
      default:
        result = { success: false, error: `\u672A\u77E5\u547D\u4EE4: ${command}` };
    }
    db.close();
  } catch (err) {
    result = { success: false, error: err.message };
  }
  console.log(JSON.stringify(result));
}
main();
