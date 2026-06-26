## 一、核心概述

### 1. **MUSA (Metaverse Unified System Architecture)**

* 摩尔线程GPU的通用并行计算平台和编程模型
* 提供GPU编程简易接口，利用GPU并行计算引擎解决复杂计算问题
* 包含MUSAToolkits：GPU加速库、运行时库、编译器、调试和优化工具

### 2. **torch\_musa**

* 基于PyTorch v2.0.0的插件形式，支持摩尔线程GPU
* 最大程度与PyTorch代码解耦，便于维护与升级
* 利用PyTorch第三方后端扩展接口，将摩尔线程高性能计算库动态注册到PyTorch
* 支持CUDA兼容特性，CUDA kernels经过porting后可运行在摩尔线程显卡上

## 二、编译安装

### 1. **依赖环境**

* Python 3.8/3.9/3.10
* MUSA软件包：驱动、Toolkits、MUDNN、MCCL、muAlg、mutlass、muThrust等
* 推荐版本：MUSA驱动2.7.0-rc4-0822，MUSAToolkits rc3.1.0

### 2. **编译流程**

1. 向PyTorch源码打patch
2. 编译PyTorch
3. 编译torch\_musa

### 3. **推荐编译方式**

<pre><div class="m_6d731127 mantine-Stack-root"><div class="p-xs bg-chatbox-background-secondary rounded-t-md border border-solid border-[var(--chatbox-border-primary)] sticky top-0 z-10 m_8bffd616 mantine-Flex-root __m__-r1cu"><div class="m_8bffd616 mantine-Flex-root __m__-r1d0"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--chatbox-tint-tertiary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="tabler-icon tabler-icon-brand-powershell "><path d="M4.887 20h11.868c.893 0 1.664 -.665 1.847 -1.592l2.358 -12c.212 -1.081 -.442 -2.14 -1.462 -2.366a1.784 1.784 0 0 0 -.385 -.042h-11.868c-.893 0 -1.664 .665 -1.847 1.592l-2.358 12c-.212 1.081 .442 2.14 1.462 2.366c.127 .028 .256 .042 .385 .042z"></path><path d="M9 8l4 4l-6 4"></path><path d="M12 16h3"></path></svg><span class="mantine-focus-auto font-mono m_b6d8b162 mantine-Text-root" data-size="sm">BASH</span></div><div class="m_8bffd616 mantine-Flex-root __m__-r1d3"><button class="mantine-focus-auto mantine-active m_8d3f4000 mantine-ActionIcon-root m_87cf2631 mantine-UnstyledButton-root" data-variant="transparent" type="button"><span class="m_8d3afb97 mantine-ActionIcon-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="tabler-icon tabler-icon-copy "><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z"></path><path d="M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></span></button></div></div><div class="border border-t-0 border-solid border-[var(--chatbox-border-primary)] rounded-b-md m_6d731127 mantine-Stack-root"><div><code class="!bg-transparent"><span class="linenumber react-syntax-highlighter-line-number">1</span><span class="token">cd</span><span> torch_musa
</span><span class="linenumber react-syntax-highlighter-line-number">2</span><span></span><span class="token">bash</span><span> build.sh  </span><span class="token"># 一键编译</span><span>
</span><span class="linenumber react-syntax-highlighter-line-number">3</span></code></div></div></div></pre>

### 4. **Docker开发环境**

* 提供开发用docker image
* 启动时需要添加`--env MTHREADS_VISIBLE_DEVICES=all`

## 三、快速入门

### 1. **常用环境变量**

* `TORCH_SHOW_CPP_STACKTRACES=1`：显示C++调用栈
* `MUDNN_LOG_LEVEL=INFO`：使能MUDNN算子库log
* `MUSA_VISIBLE_DEVICES=0,1,2,3`：控制可见显卡序号
* `MUSA_LAUNCH_BLOCKING=1`：同步模式下发MUSA kernel

### 2. **基本API使用**

<pre><div class="m_6d731127 mantine-Stack-root"><div class="p-xs bg-chatbox-background-secondary rounded-t-md border border-solid border-[var(--chatbox-border-primary)] sticky top-0 z-10 m_8bffd616 mantine-Flex-root __m__-r1dc"><div class="m_8bffd616 mantine-Flex-root __m__-r1de"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--chatbox-tint-tertiary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="tabler-icon tabler-icon-brand-python "><path d="M12 9h-7a2 2 0 0 0 -2 2v4a2 2 0 0 0 2 2h3"></path><path d="M12 15h7a2 2 0 0 0 2 -2v-4a2 2 0 0 0 -2 -2h-3"></path><path d="M8 9v-4a2 2 0 0 1 2 -2h4a2 2 0 0 1 2 2v5a2 2 0 0 1 -2 2h-4a2 2 0 0 0 -2 2v5a2 2 0 0 0 2 2h4a2 2 0 0 0 2 -2v-4"></path><path d="M11 6l0 .01"></path><path d="M13 18l0 .01"></path></svg><span class="mantine-focus-auto font-mono m_b6d8b162 mantine-Text-root" data-size="sm">PYTHON</span></div><div class="m_8bffd616 mantine-Flex-root __m__-r1dh"><button class="mantine-focus-auto mantine-active m_8d3f4000 mantine-ActionIcon-root m_87cf2631 mantine-UnstyledButton-root" data-variant="transparent" type="button"><span class="m_8d3afb97 mantine-ActionIcon-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="tabler-icon tabler-icon-copy "><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z"></path><path d="M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></span></button></div></div><div class="border border-t-0 border-solid border-[var(--chatbox-border-primary)] rounded-b-md m_6d731127 mantine-Stack-root"><div><code class="!bg-transparent"><span class="linenumber react-syntax-highlighter-line-number">1</span><span class="token">import</span><span> torch
</span><span class="linenumber react-syntax-highlighter-line-number">2</span><span></span><span class="token">import</span><span> torch_musa
</span><span class="linenumber react-syntax-highlighter-line-number">3</span>
<span class="linenumber react-syntax-highlighter-line-number">4</span><span>torch</span><span class="token">.</span><span>musa</span><span class="token">.</span><span>is_available</span><span class="token">(</span><span class="token">)</span><span>
</span><span class="linenumber react-syntax-highlighter-line-number">5</span><span>torch</span><span class="token">.</span><span>musa</span><span class="token">.</span><span>device_count</span><span class="token">(</span><span class="token">)</span><span>
</span><span class="linenumber react-syntax-highlighter-line-number">6</span><span>a </span><span class="token">=</span><span> torch</span><span class="token">.</span><span>tensor</span><span class="token">(</span><span class="token">[</span><span class="token">1.2</span><span class="token">,</span><span> </span><span class="token">2.3</span><span class="token">]</span><span class="token">,</span><span> device</span><span class="token">=</span><span class="token">'musa'</span><span class="token">)</span><span>
</span><span class="linenumber react-syntax-highlighter-line-number">7</span></code></div></div></div></pre>

### 3. **支持的功能**

* **推理**：支持常见模型如ResNet50
* **训练**：完整训练流程支持
* **混合精度训练**：支持AMP自动混合精度
* **分布式训练**：支持DDP分布式训练
* **TensorCore优化**：支持TensorFloat32加速
* **C++部署**：支持模型部署

## 四、算子开发

### 1. **算子实现分类**

* **Structured算子**：多种调用规则（functional、inplace、out）
* **UnStructured算子**：单一调用规则

### 2. **算子适配方法**

* **复用meta/impl函数（Legacy）**：复用CUDA实现
* **只复用meta函数（LegacyMeta）**：仅复用meta函数
* **自定义meta/impl函数（Customized）**：完全自定义实现
* **接入MUDNN（Customized）**：使用MUDNN库实现
* **CPU计算（Customized）**：回退到CPU计算

### 3. **CUDA-Porting机制**

* 自动将CUDA kernels转换为MUSA kernels
* 编译时自动进行，降低算子适配成本

## 五、第三方库扩展

### 1. **MUSAExtension API**

* 用于构建第三方库的MUSA扩展
* 支持CUDA代码迁移到MUSA

### 2. **扩展流程**

1. 分析构建脚本setup.py
2. 修改构建配置
3. 尝试构建并测试

## 六、性能优化

### 1. **Profiler工具**

* 适配PyTorch官方性能分析工具
* 支持单机多卡性能分析
* 可生成chrome trace文件

### 2. **TensorCore优化**

* 支持TensorFloat32加速
* 在S4000上可显著提升计算性能

## 七、调试工具

### 1. **异常算子对比和追踪工具**

* 检测算子执行异常
* 对比CPU和MUSA计算结果
* 支持分布式训练调试

### 2. **基本用法**

* 设置环境变量启用调试
* 分析日志结构和异常信息
* 处理检测到的异常

## 八、模型迁移示例（YOLOv5）

### 1. **手动迁移**

* device设置：将'cuda'改为'musa'
* DDP通信后端设置：使用'mccl'后端
* 混合精度训练设置
* 随机数种子设置

### 2. **自动迁移工具**

* **musa\_converter工具**：自动转换CUDA代码到MUSA
* 支持批量代码迁移

## 九、常见问题（FAQ）

### 1. **设备查看问题**

* 普通用户需添加至render group
* 使用`sudo usermod -aG render $(whoami)`

### 2. **计算库无法找到**

* 检查`/usr/local/musa/lib/`目录
* 设置`LD_LIBRARY_PATH`环境变量

### 3. **编译安装问题**

* 清理后重新编译：`python setup.py clean && bash build.sh`
* 可能需要更新MUSA软件栈

### 4. **Docker容器问题**

* 安装mt-container-toolkit
* 启动时添加`--env MTHREADS_VISIBLE_DEVICES=all`

### 5. **适配算子问题**

* 使用c++filt查看符号名称
* 在PyTorch源码中搜索符号
