# 大数据目录迁移到 /data（软链接模式，零破坏）

> 适用：/home 清理后仍偏大（如 ~/models 68G），需把大目录迁到大分区 /data（2.7T）。
> 2026-08-29 本机实测完成：~/models（65G）→ /data/models、~/quant-research（3.5G/13.7万文件）→ /data/quant-research，
> /home 使用率 96% → 27%，累计释放约 140G。含缓存重定向闭环（pip/npm/uv → /data/cache）。

## 核心思路
大目录迁移用 **rsync 复制 → 删原目录 → 软链接**，对路径式引用完全透明，
脚本/代码零改动（`from_pretrained("~/models/sdxl-turbo")` 这类路径自动解析到新位置）。

## 步骤

```bash
# 1. 迁移前查引用：确认只有路径式引用（脚本/cron/环境变量）
grep -rl '/home/<user>/models' ~/scripts 2>/dev/null   # 代码引用点（结果应很少）
crontab -l | grep -i models                             # cron 引用
grep -rn '/home/<user>/models' ~/.bashrc ~/.bash_profile ~/.profile 2>/dev/null  # env
# 有 grep 到 inode 级引用（lsof 打开句柄）则不能迁；路径式引用软链接透明

# 2. /data 通常 root:root 755 → 先授权（本机 sudo 免密可用）
sudo mkdir -p /data/models && sudo chown <user>:<user> /data/models

# 3. 后台同步（大目录几十 G，用 background + notify_on_complete，别前台等）
rsync -a --info=progress2 ~/models/ /data/models/
# 完成通知后核对：du -sh /data/models 与源大小一致、文件数一致

# 4. 验证后切换：删原目录 → 软链接
rm -rf ~/models && ln -s /data/models ~/models
ls -l ~/models          # 确认 -> /data/models
df -h /home /data       # 双分区复检
```

## 项目目录迁移（quant-research 实测：venv + git 仓库）
模型目录是纯数据，项目目录有 venv 和 .git，迁移后必须验证可执行：

```bash
# 1. 同步后完整性校验（13.7万文件级，2分钟完成）：
diff -rq ~/quant-research/ /data/quant-research/ | head    # 只看差异，空=一致
# 或 du -sh + find | wc -l 双侧对比；uv 缓存内 .git 空目录差异可忽略（内部结构）

# 2. 切换软链接：
rm -rf ~/quant-research && ln -s /data/quant-research ~/quant-research

# 3. 关键验证（不能省！）：
#    a) venv：/home/.../quant-research/.venv/bin/python --version
#       → venv 的 shebang 是原绝对路径，软链接保留路径故透明解析，无需重建 venv
#    b) git：cd 后 git log --oneline -1（.git 在 /data 侧，软链接路径可正常操作）
#    c) df -h /home /data 复检
```

## 缓存重定向（防止 /home 缓存再次膨胀，一次性永久生效）
pip/npm/uv 缓存会持续增长（实测 pip 13.9G + uv 2.8G），迁移后必须重定向：

```bash
sudo mkdir -p /data/cache/{pip,uv,npm} && sudo chown -R <user>:<user> /data/cache
mkdir -p ~/.config/pip
printf '[global]\ncache-dir = /data/cache/pip\n' > ~/.config/pip/pip.conf
printf 'cache=/data/cache/npm\n' > ~/.npmrc
echo 'export UV_CACHE_DIR=/data/cache/uv' >> ~/.bashrc
# 验证：
pip config get global.cache-dir    # 注意语法必须带 global. 前缀，否则报错
npm config get cache
# uv 变量新终端生效；旧缓存目录可随后手动删除
```

## 坑（本案例实测）
1. **rsync 到 root 拥有的 /data 直接报 `mkdir "/data/models" failed: Permission denied (13)`**
   ——必须先 `sudo mkdir -p` + `sudo chown <user>:<user>` 再同步；建好的目录归用户所有，
   后续增量同步（rsync 重跑）无需再 sudo。
2. **软链接前的引用核查决定方案**：如果引用是脚本里的相对/绝对路径 → 软链接 OK；
   如果是环境变量指向（如 OLLAMA_MODELS）→ 改 env 或同样软链接；如果有进程 cwd 在目录内 → 需先停进程。
3. **大目录别前台 rsync**：68G 实际耗时数分钟~十几分钟（速度波动 15~170MB/s），
   必须 `terminal(background=true, notify_on_complete=true)` 异步跑，收到完成通知再切换。
4. **pip config get 语法坑**：`pip config get cache-dir` 报 `Key does not contain dot separated section and key`，
   必须写全段名 `pip config get global.cache-dir`；venv 内 pip 同样读取用户级 ~/.config/pip/pip.conf。
5. **缓存重定向后旧缓存仍占空间**：重定向只防新增长，旧缓存（~/.cache/pip 等）需手动删除才能回收，
   确认新缓存路径已生效（pip install 后 /data/cache/pip 有写入）再删。

## 关联
- 本技能 SKILL.md「扩容分析框架」方案 A（/var/lib/docker → /data）是同思路的 daemon 级迁移
- 本机已完成迁移的大数据：/data/docker（docker data-root）、/data/ollama-models（OLLAMA 模型）、/data/agents
