# KaiwuDB 依赖项

## 编译依赖

| 依赖 | 版本 | Debian 系列包名 | RHEL 系列包名 |
|------|------|---------------|---------------|
| GCC | v7.3+ | (包含在 build-essential 中) | gcc |
| G++ | v7.3+ | (包含在 build-essential 中) | gcc-c++ |
| Make | 任意 | (包含在 build-essential 中) | make |
| Go | 1.21.13 | golang | golang |
| CMake | v3.23 | cmake | cmake |
| Autoconf | v2.68+ | autoconf | autoconf |
| Bison | 任意 | bison | bison |
| pkg-config | 任意 | pkg-config | pkg-config |
| libssl | v1.1.1+ | libssl-dev | libssl-devel |
| libncurses | v6.1+ | libncurses-dev | libncurses-devel |

## 运行时依赖

| 依赖 | 版本 | Debian 系列包名 | RHEL 系列包名 |
|------|------|---------------|---------------|
| libc6 | 任意 | libc6 | glibc |
| libgcc | v7.3.0+ | libgcc1 | libgcc |
| libstdc++ | v7.3.0+ | libstdc++6 | libstdc++ |
| libatomic | v7.3.0+ | libatomic1 | (包含在 libgcc 中) |
| libz | v1.2.0+ | zlib1g | zlib |

## 建议性依赖

| 依赖 | 版本 | Debian 系列包名 | RHEL 系列包名 |
|------|------|---------------|---------------|
| geos | v3.12+ | libgeos-c1t64 | geos |

## Ubuntu 22.04 / Debian 系列快速安装

```bash
apt-get update && apt-get install -y \
    build-essential \
    cmake \
    autoconf \
    golang \
    bison \
    libssl-dev \
    libncurses5-dev \
    libgeos-dev
```

## 第三方依赖（源码引入）

以下依赖已改为从源码编译，不再需要单独安装：
- protobuf
- gflags
- lz4
- brpc
