/**
 * 性能监控管理器
 * 监控和记录系统性能指标
 */

const { DatabaseManager } = require('./database-manager');

class PerformanceMonitor {
  constructor(dbPath = null) {
    this.db = new DatabaseManager(dbPath).getDb();
    this.metrics = new Map();
  }

  /**
   * 初始化性能监控表
   */
  async initPerformanceMonitoring() {
    try {
      const createTableSQL = `
        CREATE TABLE IF NOT EXISTS performance_metrics (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          metric_name TEXT NOT NULL,
          metric_value REAL NOT NULL,
          metric_type TEXT NOT NULL DEFAULT 'GAUGE',
          tags TEXT,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
          description TEXT
        );
      `;
      
      this.db.run(createTableSQL);
      
      // 创建索引
      this.db.run(`
        CREATE INDEX IF NOT EXISTS idx_metric_name 
        ON performance_metrics(metric_name);
      `);
      
      this.db.run(`
        CREATE INDEX IF NOT EXISTS idx_timestamp 
        ON performance_metrics(timestamp);
      `);
      
      this.db.run(`
        CREATE INDEX IF NOT EXISTS idx_metric_type 
        ON performance_metrics(metric_type);
      `);
      
      console.log('✅ 性能监控表初始化完成');
      return true;
    } catch (error) {
      console.error('❌ 初始化性能监控表失败:', error.message);
      return false;
    }
  }

  /**
   * 记录性能指标
   */
  async recordMetric(metricName, value, options = {}) {
    try {
      const metricType = options.type || 'GAUGE';
      const tags = options.tags ? JSON.stringify(options.tags) : null;
      const description = options.description || null;
      
      const insertSQL = `
        INSERT INTO performance_metrics 
        (metric_name, metric_value, metric_type, tags, description)
        VALUES (?, ?, ?, ?, ?);
      `;
      
      this.db.run(insertSQL, metricName, value, metricType, tags, description);
      
      // 更新内存中的指标
      this.metrics.set(metricName, {
        value: value,
        timestamp: new Date(),
        type: metricType,
        tags: options.tags || {}
      });
      
      return true;
    } catch (error) {
      console.error('❌ 记录性能指标失败:', error.message);
      return false;
    }
  }

  /**
   * 记录任务执行时间
   */
  async recordTaskExecution(taskId, duration, agentName = null) {
    try {
      const tags = agentName ? { agent: agentName, task: taskId } : { task: taskId };
      
      await this.recordMetric('task_execution_time', duration, {
        type: 'GAUGE',
        tags: tags,
        description: `任务 ${taskId} 执行时间`
      });
      
      console.log(`✅ 已记录任务 ${taskId} 执行时间：${duration}ms`);
      return true;
    } catch (error) {
      console.error('❌ 记录任务执行时间失败:', error.message);
      return false;
    }
  }

  /**
   * 记录数据库查询时间
   */
  async recordDatabaseQuery(queryType, duration, rowsAffected = 0) {
    try {
      const tags = { type: queryType, rows: rowsAffected };
      
      await this.recordMetric('database_query_time', duration, {
        type: 'GAUGE',
        tags: tags,
        description: `${queryType} 查询时间`
      });
      
      return true;
    } catch (error) {
      console.error('❌ 记录数据库查询时间失败:', error.message);
      return false;
    }
  }

  /**
   * 记录系统资源使用
   */
  async recordSystemResources(cpu = 0, memory = 0, disk = 0) {
    try {
      await this.recordMetric('cpu_usage', cpu, {
        type: 'GAUGE',
        tags: { unit: 'percent' },
        description: 'CPU 使用率'
      });
      
      await this.recordMetric('memory_usage', memory, {
        type: 'GAUGE',
        tags: { unit: 'percent' },
        description: '内存使用率'
      });
      
      await this.recordMetric('disk_usage', disk, {
        type: 'GAUGE',
        tags: { unit: 'percent' },
        description: '磁盘使用率'
      });
      
      return true;
    } catch (error) {
      console.error('❌ 记录系统资源使用失败:', error.message);
      return false;
    }
  }

  /**
   * 获取指标历史数据
   */
  async getMetricHistory(metricName, hours = 24) {
    try {
      const querySQL = `
        SELECT * FROM performance_metrics
        WHERE metric_name = ?
        AND timestamp > datetime('now', ? || ' hours')
        ORDER BY timestamp ASC;
      `;
      
      const history = this.db.all(querySQL, metricName, `-${hours}`);
      return history || [];
    } catch (error) {
      console.error('❌ 获取指标历史失败:', error.message);
      return [];
    }
  }

  /**
   * 获取指标统计
   */
  async getMetricStats(metricName, hours = 24) {
    try {
      const querySQL = `
        SELECT 
          metric_name,
          COUNT(*) as count,
          MIN(metric_value) as min_value,
          MAX(metric_value) as max_value,
          AVG(metric_value) as avg_value,
          MIN(timestamp) as first_recorded,
          MAX(timestamp) as last_recorded
        FROM performance_metrics
        WHERE metric_name = ?
        AND timestamp > datetime('now', ? || ' hours')
        GROUP BY metric_name;
      `;
      
      const stats = this.db.get(querySQL, metricName, `-${hours}`);
      return stats || null;
    } catch (error) {
      console.error('❌ 获取指标统计失败:', error.message);
      return null;
    }
  }

  /**
   * 获取所有指标统计
   */
  async getAllMetricsStats(hours = 24) {
    try {
      const querySQL = `
        SELECT 
          metric_name,
          metric_type,
          COUNT(*) as count,
          MIN(metric_value) as min_value,
          MAX(metric_value) as max_value,
          AVG(metric_value) as avg_value,
          MIN(timestamp) as first_recorded,
          MAX(timestamp) as last_recorded
        FROM performance_metrics
        WHERE timestamp > datetime('now', ? || ' hours')
        GROUP BY metric_name, metric_type
        ORDER BY last_recorded DESC;
      `;
      
      const stats = this.db.all(querySQL, `-${hours}`);
      return stats || [];
    } catch (error) {
      console.error('❌ 获取所有指标统计失败:', error.message);
      return [];
    }
  }

  /**
   * 获取性能报告
   */
  async getPerformanceReport(hours = 24) {
    try {
      const report = {
        summary: {},
        metrics: {},
        alerts: []
      };
      
      // 获取所有指标统计
      const allStats = await this.getAllMetricsStats(hours);
      
      // 按指标名称分组
      for (const stat of allStats) {
        if (!report.metrics[stat.metric_name]) {
          report.metrics[stat.metric_name] = {
            type: stat.metric_type,
            count: stat.count,
            min: stat.min_value,
            max: stat.max_value,
            avg: stat.avg_value,
            first_recorded: stat.first_recorded,
            last_recorded: stat.last_recorded
          };
        }
      }
      
      // 生成摘要
      report.summary = {
        total_metrics: Object.keys(report.metrics).length,
        total_records: allStats.reduce((sum, stat) => sum + stat.count, 0),
        time_range: {
          hours: hours,
          start: new Date(Date.now() - hours * 60 * 60 * 1000).toISOString(),
          end: new Date().toISOString()
        }
      };
      
      // 检查异常指标
      const thresholds = {
        'cpu_usage': { warning: 80, critical: 95 },
        'memory_usage': { warning: 80, critical: 95 },
        'disk_usage': { warning: 80, critical: 95 },
        'task_execution_time': { warning: 10000, critical: 60000 }
      };
      
      for (const [metricName, threshold] of Object.entries(thresholds)) {
        if (report.metrics[metricName]) {
          const max = report.metrics[metricName].max;
          if (max >= threshold.critical) {
            report.alerts.push({
              metric: metricName,
              level: 'CRITICAL',
              value: max,
              threshold: threshold.critical,
              message: `${metricName} 超过临界值：${max} >= ${threshold.critical}`
            });
          } else if (max >= threshold.warning) {
            report.alerts.push({
              metric: metricName,
              level: 'WARNING',
              value: max,
              threshold: threshold.warning,
              message: `${metricName} 超过警告值：${max} >= ${threshold.warning}`
            });
          }
        }
      }
      
      return report;
    } catch (error) {
      console.error('❌ 生成性能报告失败:', error.message);
      return null;
    }
  }

  /**
   * 清理旧的性能数据
   */
  async cleanupOldMetrics(days = 7) {
    try {
      const deleteSQL = `
        DELETE FROM performance_metrics
        WHERE timestamp < datetime('now', ? || ' days');
      `;
      
      const deleteStmt = this.db.prepare(deleteSQL);
      const result = deleteStmt.run(`-${days}`);
      
      console.log(`✅ 已清理 ${result.changes} 条旧性能数据`);
      return result.changes;
    } catch (error) {
      console.error('❌ 清理旧性能数据失败:', error.message);
      return 0;
    }
  }

  /**
   * 启动性能监控定时任务
   */
  startMonitoringLoop(interval = 60000) {
    console.log('🔄 启动性能监控定时任务...');
    
    setInterval(async () => {
      try {
        // 记录系统资源
        const os = require('os');
        const cpuUsage = os.loadavg()[0] / os.cpus().length * 100;
        const memoryUsage = (1 - os.freemem() / os.totalmem()) * 100;
        
        await this.recordSystemResources(cpuUsage, memoryUsage, 0);
        
        // 生成性能报告
        const report = await this.getPerformanceReport(1);
        
        if (report.alerts.length > 0) {
          console.log('\n=== 性能告警 ===');
          for (const alert of report.alerts) {
            console.log(`[${alert.level}] ${alert.message}`);
          }
        }
        
      } catch (error) {
        console.error('❌ 性能监控循环失败:', error.message);
      }
    }, interval);
  }

  /**
   * 获取当前内存中的指标快照
   */
  getMetricsSnapshot() {
    const snapshot = {};
    
    for (const [name, metric] of this.metrics) {
      snapshot[name] = {
        value: metric.value,
        timestamp: metric.timestamp,
        type: metric.type,
        tags: metric.tags
      };
    }
    
    return snapshot;
  }

  /**
   * 导出性能数据为 JSON
   */
  async exportMetricsToFile(filename = 'performance-export.json', hours = 24) {
    try {
      const fs = require('fs');
      const report = await this.getPerformanceReport(hours);
      
      const exportData = {
        exported_at: new Date().toISOString(),
        time_range: report.summary.time_range,
        metrics: report.metrics,
        alerts: report.alerts
      };
      
      fs.writeFileSync(filename, JSON.stringify(exportData, null, 2));
      console.log(`✅ 性能数据已导出到 ${filename}`);
      return true;
    } catch (error) {
      console.error('❌ 导出性能数据失败:', error.message);
      return false;
    }
  }
}

module.exports = { PerformanceMonitor };
