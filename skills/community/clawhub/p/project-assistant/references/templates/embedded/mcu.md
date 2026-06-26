# 嵌入式MCU项目分析

分析嵌入式MCU项目（STM32/ESP32/Arduino等），生成项目文档。

## 适用类型

- `stm32` - STM32项目 (HAL/LL)
- `esp32` - ESP-IDF项目
- `arduino` - Arduino项目
- `pico` - Raspberry Pi Pico
- `keil` - Keil MDK项目
- `iar` - IAR项目
- `platformio` - PlatformIO项目

## 执行步骤

### 1. 识别MCU型号

检查文件：
- `*.ioc` → STM32CubeMX配置，解析获取MCU
- `sdkconfig` → ESP-IDF配置，解析 CONFIG_IDF_TARGET
- `platformio.ini` → [env]段获取 board/mcu
- `*.ld` → 链接脚本，解析MEMORY区域
- `*.h` → 检查 `#define STM32F4xx` 等宏

### 2. 解析内存布局

调用链接脚本解析器：
```bash
python3 ~/.claude/tools/init/parsers/linker_parser.py "$TARGET_DIR"
```

提取：
- FLASH起始地址和大小
- RAM起始地址和大小
- 特殊段配置

### 3. 分析外设使用

扫描代码中的HAL/LL调用：
- `HAL_UART_*` / `LL_USART_*` → UART
- `HAL_SPI_*` / `LL_SPI_*` → SPI
- `HAL_I2C_*` / `LL_I2C_*` → I2C
- `HAL_GPIO_*` → GPIO
- `HAL_ADC_*` → ADC
- `HAL_TIM_*` → Timer/PWM
- `HAL_CAN_*` → CAN
- `HAL_ETH_*` / `lwip` → 以太网

### 4. 检测RTOS

检查特征：
- `#include "FreeRTOS.h"` → FreeRTOS
- `#include <zephyr.h>` → Zephyr
- `#include "rtthread.h"` → RT-Thread

如有RTOS，调用RTOS解析器：
```bash
python3 ~/.claude/tools/init/parsers/rtos_parser.py "$TARGET_DIR"
```

### 5. 分析模块结构

典型目录结构：
```
project/
├── Core/           # 主程序
│   ├── Src/
│   └── Inc/
├── Drivers/        # 驱动库
│   ├── STM32xx_HAL_Driver/
│   └── CMSIS/
├── Middlewares/    # 中间件
├── App/            # 应用层
│   ├── Modules/
│   └── Utils/
└── Build/          # 构建输出
```

### 6. 生成文档

使用模板：`~/.claude/commands/init/templates/project-template.md`

嵌入式扩展部分包含：
- MCU型号和规格
- 内存布局表
- 外设使用表
- RTOS配置（如有）

## 输出格式

```
项目初始化完成！

项目名称: {name}
项目类型: 嵌入式固件
主要语言: C
框架/平台: {HAL/Arduino/ESP-IDF}
构建系统: {CMake/Makefile/Keil}
目标平台: {MCU型号} ({ARCH}, {FREQ}, {FLASH} Flash, {RAM} RAM)

模块统计:
  - 核心模块: {count} 个
  - 驱动模块: {count} 个

外设使用:
  - {peripheral1}: {usage}
  - {peripheral2}: {usage}

RTOS: {FreeRTOS/无}

核心功能: {count} 项
  1. {feature1}
  2. {feature2}

已生成项目文档: .claude/project.md
```