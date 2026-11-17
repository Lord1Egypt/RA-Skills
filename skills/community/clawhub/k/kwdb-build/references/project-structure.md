# KaiwuDB 项目结构

## 目录布局

```
KaiwuDB/
├── CMakeLists.txt          # 根 CMake 配置
├── Makefile                # 根 Makefile，包含构建目标
├── README.md               # 项目文档
├── NOTICE.txt              # 许可证声明
│
├── common/                 # 共享 C++ 工具库
│   ├── CMakeLists.txt
│   └── src/
│
├── kwdbts2/                # C++ 时序引擎（主要部分）
│   ├── CMakeLists.txt
│   ├── include/            # 公共头文件
│   ├── engine/            # 存储引擎
│   ├── exec/              # 查询执行
│   ├── storage/           # 存储层
│   ├── ts_engine/        # 时序引擎
│   ├── statistic/         # 统计信息
│   ├── common/            # 内部公共模块
│   ├── mmap/              # 内存映射文件
│   ├── roachpb/           # 协议缓冲区
│   ├── brpc/              # brpc 库
│   ├── shell/             # 命令行 shell
│   └── third_party/       # 第三方依赖
│
├── kwbase/                 # Go 语言关系型数据库
│   ├── Makefile
│   ├── Makefile_ent       # 企业版 Makefile
│   ├── pkg/               # Go 包
│   ├── c-deps/            # C 依赖
│   ├── vendor/            # Go 依赖
│   └── build/             # 构建输出
│
├── kwdbml/                 # 机器学习组件
│
├── SDK/                    # SDK 头文件和库
│   ├── CMakeLists.txt
│   └── ...
│
├── build/                  # CMake 构建目录
│   ├── CMakeCache.txt
│   ├── CMakeFiles/
│   ├── common/
│   ├── kwdbts2/
│   └── lib/
│
├── install/                # 安装输出
│   ├── bin/               # 可执行文件 (kwbase)
│   └── lib/               # 共享库 (libcommon.so, libkwdbts2.so, libopentelemetry.so)
│
├── cluster_start/          # 集群启动脚本
│   └── utils.sh
│
├── qa/                     # QA 和测试脚本
│   ├── run_test_v2.sh
│   ├── run_test_local_v2.sh
│   ├── run_tsbs_test.sh
│   └── env.sh
│
└── kaiwudb_install/        # 安装脚本
    ├── deploy.sh
    └── add_user.sh
```

## 主要组件

### kwdbts2 (C++ 时序引擎)
主要的数据库引擎，使用 C++ 编写。包含：
- **include/** - 公共 API 头文件
- **engine/** - 核心存储引擎实现
- **exec/** - 查询执行器
- **storage/** - 存储子系统
- **ts_engine/** - 时序专用引擎
- **statistic/** - 统计信息收集
- **mmap/** - 内存映射文件处理
- **roachpb/** - 协议缓冲区定义

### kwbase (Go)
关系型数据库组件：
- **pkg/** - Go 包（sql, kv, storage 等）
- **c-deps/** - Go 使用的 C 依赖
- **vendor/** - Go 依赖

### common (C++)
kwdbts2 和 kwbase 共用的工具库：
- 内存管理
- 日志
- 通用数据结构

## 构建产物

构建完成后，产物位于：
- **install/bin/** - 可执行文件 (kwbase 等)
- **install/lib/** - 共享库 (libcommon.so, libkwdbts2.so, libopentelemetry.so)
