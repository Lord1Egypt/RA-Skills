# 服务部署配方与排障

两条路线的参数模板、服务化写法与排障对照表。占位符统一用 `$MODELDECK_HOME`（Windows 上为 `%MODELDECK_HOME%`），使用时替换成你的数据目录。

## 一、Ollama 路线

### 环境变量

| 变量 | 作用 | 建议值 | 说明 |
|---|---|---|---|
| `OLLAMA_MODELS` | 权重与清单目录 | `$MODELDECK_HOME/models` | 必须在服务进程的环境里生效，写在别的脚本里不算 |
| `OLLAMA_HOST` | 监听地址 | `0.0.0.0:11434` | 只给本机用就写 `127.0.0.1:11434` |
| `OLLAMA_KEEP_ALIVE` | 空闲后保留多久 | `30m` | 太短反复冷加载，太长一直占显存 |
| `OLLAMA_NUM_PARALLEL` | 单模型并行请求数 | `2` | 每个槽位各占一份 KV，要回算预算 |
| `OLLAMA_MAX_LOADED_MODELS` | 同时驻留模型数 | `1` | 大于 1 会双份占显存 |
| `OLLAMA_FLASH_ATTENTION` | flash attention | `1` | 量化 KV 的前置条件，不开启时 `q8_0` 设置不生效 |
| `OLLAMA_KV_CACHE_TYPE` | KV 精度 | `q8_0` | 可选 `f16`、`q8_0`、`q4_0` |

### Modelfile 模板

```text
FROM <暂存目录>/model-Q4_K_M.gguf
PARAMETER num_ctx 8192
PARAMETER num_gpu 99
PARAMETER num_predict 1024
PARAMETER temperature 0.7
```

`num_ctx` 是服务端真正生效的上下文，请求侧改不动；`num_gpu` 是卸载到显存的层数，`99` 表示能卸多少卸多少；`num_predict` 是默认输出上限，推理模型要显著调大。

```bash
ollama create local-model:q4 -f Modelfile
curl -s http://127.0.0.1:11434/api/tags && curl -s http://127.0.0.1:11434/v1/models
```

### 服务化

Linux（systemd）：

```bash
sudo systemctl edit ollama
# [Service]
# Environment="OLLAMA_MODELS=/data/modeldeck/models"
# Environment="OLLAMA_KV_CACHE_TYPE=q8_0"
# Environment="OLLAMA_FLASH_ATTENTION=1"
sudo systemctl daemon-reload && sudo systemctl restart ollama
systemctl show ollama -p Environment     # 确认变量真的进了进程
```

Windows：环境变量写进 `.cmd`，再由计划任务或启动目录调用，别依赖当前终端会话：

```bat
@echo off
rem 把目录换成你自己的数据目录
set MODELDECK_HOME=D:\modeldeck
set OLLAMA_MODELS=%MODELDECK_HOME%\models
set OLLAMA_KV_CACHE_TYPE=q8_0
set OLLAMA_FLASH_ATTENTION=1
"%MODELDECK_HOME%\bin\ollama.exe" serve
```

macOS：用 `brew services start ollama` 托管，环境变量写进 launchd plist 的 `EnvironmentVariables`；`~/.zshrc` 只对交互终端生效，对后台服务无效。

## 二、llama.cpp 路线

### 编译与获取

```bash
# Linux + CUDA
cmake -B build -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release && cmake --build build --config Release -j
# macOS：Metal 默认开启
cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build --config Release -j
```

也可以用官方预编译包，但**构建产物必须与驱动支持的 CUDA 大版本匹配**：错配时可能不报错地回落到纯 CPU，表现为"能跑但极慢"。验证方法见排障表第一行。

### 关键参数

| 参数 | 作用 | 调大 | 调小 |
|---|---|---|---|
| `-ngl` | 卸载到 GPU 的层数 | 越快，越吃显存 | 越慢，越省显存 |
| `-c` | 上下文长度 | 支持更长输入，KV 线性增长 | 省显存，长文被截断 |
| `-fa on` | flash attention（旧版写作 `--flash-attn`） | 省显存、加速长上下文 | KV 占用上升 |
| `--cache-type-k/v` | KV 精度 | `f16` 精度最高 | `q8_0`、`q4_0` 省显存 |
| `-np` | 并行槽位 | 提高并发吞吐 | 降低显存占用 |
| `-t` | CPU 线程数 | 接近物理核数 | 过多互相争抢 |
| `-b` / `-ub` | 批大小 | 加速预填充 | 降低峰值内存 |
| `--jinja` | 用 GGUF 内嵌对话模板 | 正确解析角色与工具调用 | 退化为裸拼接 |
| `--no-kv-offload` | KV 留在内存 | 换出显存 | 长上下文变慢 |

### 三档模板

```bash
# 小显存（8 GB 级）：短上下文 + 量化 KV + 单槽
llama-server -m "$MODELDECK_HOME/models/model-Q4_K_M.gguf" --host 127.0.0.1 --port 8080 \
  -c 4096 -ngl 99 -fa on --cache-type-k q8_0 --cache-type-v q8_0 -np 1 --jinja

# 中等显存（16–24 GB 级）：标准上下文 + 双槽
llama-server -m "$MODELDECK_HOME/models/model-Q4_K_M.gguf" --host 0.0.0.0 --port 8080 \
  -c 16384 -ngl 99 -fa on --cache-type-k q8_0 --cache-type-v q8_0 -np 2 --cont-batching --jinja --metrics

# CPU / Apple Silicon：全层卸载交给 Metal，或纯 CPU 用物理核数
llama-server -m "$MODELDECK_HOME/models/model-Q4_K_M.gguf" --host 127.0.0.1 --port 8080 \
  -c 8192 -ngl 99 -fa on -t 1 --jinja
```

### systemd 单元与反向代理

```ini
[Service]
Environment=MODELDECK_HOME=/data/modeldeck
ExecStart=/data/modeldeck/bin/llama-server -m /data/modeldeck/models/model-Q4_K_M.gguf \
  --host 127.0.0.1 --port 8080 -c 16384 -ngl 99 -fa on --jinja --metrics
Restart=always
RestartSec=5
```

```nginx
location /v1/ {
    proxy_pass http://127.0.0.1:8080/v1/;
    proxy_buffering off;          # 不关会把 SSE 攒成一整块，前端看不到逐字输出
    proxy_read_timeout 600s;
    proxy_http_version 1.1;
}
```

## 三、排障对照表

| 现象 | 最可能原因 | 处置 |
|---|---|---|
| 加载即 OOM，显存看着够 | 上下文过大或 KV 未量化 | 降 `-c`、加 `--cache-type-k q8_0`、降 `-ngl` |
| 加载成功，长提示进来就 OOM | KV 随上下文增长 | 降上下文或降 KV 精度 |
| 健康检查通但极慢 | 二进制与 CUDA 版本错配、回落 CPU | 换匹配构建产物，用 `nvidia-smi` 确认进程 |
| 输出乱码或重复 | 对话模板未生效 / 温度过高 / 量化过狠 | 加 `--jinja`、降温度、升量化档 |
| 首 token 很久，之后很快 | 预填充慢（正常现象） | 缩短系统提示、减少历史、提高批大小 |
| 上下文超限报错 | 请求侧与服务端不一致 | 统一上下文值，重建模型或加 `-c` |
| 流式一直不结束 | 中间层缓冲或未分块传输 | 关 `proxy_buffering`，确认分块传输 |
| 客户端报缺 API key | 客户端库要求非空 | 填任意非空占位串 |
| 并发时全部变慢 | 单模型排队，槽位不足 | 加 `-np` 并回算显存 |
| 重启后显存没释放 | 残留子进程 | 按 PID 结束，确认显存回落到接近 0 |
