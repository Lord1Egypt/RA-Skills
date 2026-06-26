# RTOS项目分析

分析FreeRTOS、Zephyr、RT-Thread等RTOS项目。

## 适用类型

- `freertos` - FreeRTOS项目
- `zephyr` - Zephyr RTOS项目
- `rt-thread` - RT-Thread项目

## 执行步骤

### 1. 识别RTOS类型

检查头文件：
- `#include "FreeRTOS.h"` → FreeRTOS
- `#include <zephyr.h>` 或 `#include <zephyr/kernel.h>` → Zephyr
- `#include "rtthread.h"` → RT-Thread

### 2. 解析RTOS配置

#### FreeRTOS
解析 `FreeRTOSConfig.h`:
- `configUSE_PREEMPTION`
- `configTICK_RATE_HZ`
- `configMAX_PRIORITIES`
- `configTOTAL_HEAP_SIZE`
- `configUSE_MUTEXES`, `configUSE_SEMAPHORES`

#### Zephyr
解析 `prj.conf` 或 `Kconfig`:
- `CONFIG_THREAD_NAME`
- `CONFIG_NUM_COOP_PRIORITIES`
- `CONFIG_HEAP_MEM_POOL_SIZE`

#### RT-Thread
解析 `rtconfig.h`:
- `RT_THREAD_PRIORITY_MAX`
- `RT_TICK_PER_SECOND`
- `RT_USING_MUTEX`, `RT_USING_SEMAPHORE`

### 3. 分析任务/线程

调用RTOS解析器：
```bash
python3 ~/.claude/tools/init/parsers/rtos_parser.py "$TARGET_DIR"
```

提取：
- 任务名称和优先级
- 堆栈大小
- 任务函数

### 4. 分析IPC机制

检测使用：
- 信号量 (`xSemaphoreCreate*`, `rt_sem_create`)
- 互斥量 (`xSemaphoreCreateMutex`, `rt_mutex_create`)
- 队列 (`xQueueCreate`, `rt_mq_create`)
- 事件组 (`xEventGroupCreate`, `rt_event_create`)
- 定时器 (`xTimerCreate`, `rt_timer_create`)

### 5. 生成文档

使用模板：`~/.claude/commands/init/templates/project-template.md`

RTOS扩展部分：
- 任务列表及配置
- IPC使用情况
- 内存配置

## 输出格式

```
项目初始化完成！

项目名称: {name}
项目类型: 嵌入式RTOS固件
主要语言: C
框架/平台: {RTOS名称}
构建系统: {CMake/Makefile}
目标平台: {MCU型号}

RTOS配置:
  - 调度方式: {抢占/协作}
  - 时钟频率: {HZ} Hz
  - 最大优先级: {num}
  - 堆大小: {size} KB

任务统计:
  - 任务数: {count} 个
  - 总堆栈: {size} KB

IPC使用:
  - 信号量: {count} 个
  - 队列: {count} 个
  - 定时器: {count} 个

核心功能: {count} 项

已生成项目文档: .claude/project.md
```