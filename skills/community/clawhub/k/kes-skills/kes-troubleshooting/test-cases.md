# KingbaseES 故障排查测试用例

## 集群状态异常

### TC-001：节点状态异常检测

**场景**：集群中某节点 status 变为 non-running

**步骤**：
1. 执行 `repmgr cluster show` 查看集群状态
2. 发现某节点 status 非 running
3. 查看该节点 `kbha.log` 日志
4. 查看 `sys_log/` 数据库日志
5. 判断关库原因（网关故障/磁盘故障/coredump/其他）

**预期**：能够快速定位关库原因

### TC-002：双主故障处理

**场景**：集群出现双主，两个节点都显示为 primary

**步骤**：
1. 执行 `repmgr cluster show` 确认双主状态
2. 在各主库执行 `select sys_current_wal_lsn();` 对比数据量
3. 通过业务数据确认最新主库
4. 暂停集群：`repmgr service pause`
5. 关闭数据较少的主库：`sys_ctl -D data stop`
6. 取消暂停：`repmgr service unpause`
7. 恢复原主库为备库：`kbha -A rejoin -h ${新主库IP}`

**预期**：双主消除，集群恢复正常

### TC-003：时间线冲突处理

**场景**：数据库无法启动，报 "requested timeline X is not a child of this server's history"

**步骤**：
1. 查看日志确认 timeline 错误信息
2. 执行 `sys_controldata -D data` 获取控制文件中记录的 TimeLineID
3. 删除 `data/sys_wal/` 和归档目录中高于该 TimeLineID 的 history 文件
4. 启动数据库

**预期**：数据库正常启动

### TC-004：WAL 缺失导致备库启动失败

**场景**：备库报 "requested WAL segment has already been removed"

**步骤**：
1. 查看备库日志确认缺失的 WAL 段
2. 在主库执行 `repmgr service pause`
3. 在备库执行 `repmgr standby clone -F -h ${主库IP} -U esrep -d esrep -p ${主库端口} --fast-checkpoint`
4. 启动数据库：`sys_ctl -D data start`
5. 重新注册：`repmgr standby register -F`
6. 取消暂停：`repmgr service unpause`

**预期**：备库恢复正常流复制

## 资源耗尽

### TC-005：连接数耗尽

**场景**：新连接被拒绝，报 "too many connections"

**步骤**：
1. 查询当前连接数：`SELECT count(*) FROM sys_stat_activity;`
2. 查看 max_connections：`SHOW max_connections;`
3. 找出占用连接多的应用：`SELECT application_name, count(*) FROM sys_stat_activity GROUP BY application_name;`
4. 终止空闲连接或调整连接池参数

**预期**：连接数恢复正常

### TC-006：长事务检测

**场景**：事务号 age 持续增长

**步骤**：
1. 查询最长事务：`SELECT pid, datname, query, age(backend_xmin) FROM sys_stat_activity WHERE backend_xmin IS NOT NULL ORDER BY age(backend_xmin) DESC LIMIT 1;`
2. 判断长事务来源（客户端工具/应用/两阶段提交）
3. 终止长事务连接

**预期**：事务号增长停止

### TC-007：存储容量耗尽

**场景**：数据库目录磁盘空间不足

**步骤**：
1. 检查各目录容量：`df -h`
2. 分析数据增长原因（表膨胀/WAL 堆积/归档未清理/临时文件残留）
3. 紧急处理：删除残留临时文件、清理归档
4. 完整处理：扩容存储、优化检查点参数

**预期**：磁盘空间恢复正常

## 性能诊断

### TC-008：慢 SQL 排查

**场景**：业务反馈查询响应慢

**步骤**：
1. 配置慢 SQL 日志：`set Log_min_duration_statement = 1000;`
2. 收集当前活动连接：`select * from sys_stat_activity;`
3. 使用 KWR 收集性能快照
4. 分析执行计划：`EXPLAIN ANALYZE <慢SQL>;`
5. 根据执行计划优化（添加索引/改写 SQL/更新统计信息）

**预期**：定位慢 SQL 原因并提供优化方案

### TC-009：CPU 使用率过高

**场景**：CPU 利用率持续超过 70%

**步骤**：
1. 使用 nmon 采集 CPU 数据
2. 使用 `top -o %CPU` 查看高 CPU 进程
3. 收集 KWR 报告，分析 TOP SQL
4. 对 CPU 消耗大的 SQL 进行优化

**预期**：识别 CPU 消耗来源并优化

## 数据安全

### TC-010：备份验证

**场景**：定期检查备份可用性和完整性

**步骤**：
1. 执行 `sys_rman --config=/path/sys_rman.conf --stanza=kingbase info`
2. 执行 `sys_rman --config=/path/sys_rman.conf --stanza=kingbase check`
3. 确认无报错信息

**预期**：备份配置和归档正常

### TC-011：数据库无响应（D 态进程）

**场景**：数据库进程无响应，连接超时

**步骤**：
1. `top` 查看进程状态，确认 S 列为 D
2. 采集进程调用栈：`pstack <PID>`
3. 检查 I/O 子系统：`iostat -x 1`
4. 协调 OS 工程师排查存储问题

**预期**：定位 I/O 子系统问题
