---
name: kes-c-odbc
name_for_command: kes-c-odbc
description: 指导用户完成C/ODBC/DCI连接KingbaseES数据库。当用户提到C语言开发、KCI原生接口、ODBC连接、ESQL/C嵌入式SQL、DCI、libkci编译链接、unixODBC时，必须使用此技能。
---

# KingbaseES C 语言接口指南

本技能指导用户完成 C 语言连接 KingbaseES 的完整流程，涵盖 KCI 原生接口、ODBC 标准接口和 DCI (ESQL/C) 嵌入式 SQL。

## 接口选型

| 接口 | 适用场景 | 库文件 |
|------|---------|--------|
| KCI (libkci) | 原生 C 应用，追求性能 | `libkci.so` |
| ODBC | BI 工具集成、跨平台、遗留系统 | `kdbodbcw.so` |
| DCI (ESQL/C) | Oracle OCI 兼容迁移 | `libdcikdb.so` |

## 支持环境

- **Linux 架构**: x86_64、ARM64、LoongArch、MIPS、SW64
- **Windows**: V9 提供 64 位支持
- **编译器**: Linux 仅支持 glibc，Windows 依赖 msvc120

---

## KCI 原生接口

KingbaseES 提供的原生 C 数据库访问库。

**库文件位置**：`$KINGBASE_HOME/lib/libkci.so`

### 编译链接

```bash
gcc -I $KINGBASE_HOME/include -L $KINGBASE_HOME/lib myapp.c -o myapp -lkci -Wl,-rpath,$KINGBASE_HOME/lib
```

**Makefile 示例**：
```makefile
CPPFLAGS += -I $(KINGBASE_HOME)/include
LDFLAGS  += -L $(KINGBASE_HOME)/lib
LIBS     += -lkci
```

### 代码示例

```c
#include <stdio.h>
#include <stdlib.h>
#include "libkci_fe.h"

int main() {
    char connInfo[] = "host=127.0.0.1 port=54321 user=system password=123456 dbname=test";
    KCIConnection *conn = KCIConnectionCreate(connInfo);

    if (KCIConnectionGetStatus(conn) != CONNECTION_OK) {
        fprintf(stderr, "Connect error: %s\n", KCIConnectionGetLastError(conn));
        KCIConnectionDestory(conn);
        return 1;
    }

    KCIResult *res = KCIStatementExecute(conn, "SELECT version()");
    for (int i = 0; i < KCIResultGetRowCount(res); i++) {
        for (int j = 0; j < KCIResultGetColumnCount(res); j++) {
            printf("| %s ", KCIResultGetColumnValue(res, i, j));
        }
        printf("\n");
    }
    KCIResultDealloc(res);
    KCIConnectionDestory(conn);
    return 0;
}
```

### 连接串格式

```c
// 键值对形式
"host=127.0.0.1 port=54321 user=system password=123456 dbname=test"

// URL 形式
"kingbase://system:123456@127.0.0.1:54321/test"
```

---

## ODBC 标准接口

### Linux 部署

1. 安装 unixODBC（推荐 2.3.4）：
```bash
./configure --prefix=$(pwd)/release && make && make install
```

2. 配置 `odbcinst.ini`：
```ini
[kdbodbc test driver]
Description = KingbaseES ODBC driver (Unicode version)
Driver = /path/to/kdbodbcw.so
```

3. 配置 `odbc.ini`：
```ini
[KingbaseES]
Description  = KingbaseES DSN
Driver       = kdbodbc test driver
Servername   = 127.0.0.1
Port         = 54321
Username     = system
Password     = 123456
Database     = test
```

4. 设置环境变量：
```bash
export ODBCSYSINI=.
export ODBCINI=./odbc.ini
```

5. 测试连接：`isql KingbaseES`

### Windows 部署

1. 创建 `.reg` 文件注册 ODBC 驱动：
```reg
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\ODBC\ODBCINST.INI\ODBC Drivers]
"KingbaseES 9 ODBC Driver ANSI"="Installed"

[HKEY_LOCAL_MACHINE\SOFTWARE\ODBC\ODBCINST.INI\KingbaseES 9 ODBC Driver ANSI]
"Driver"="D:\\path\\to\\kdbodbc30a.dll"
"Setup"="D:\\path\\to\\kdbodbc30a.dll"
```

2. 打开 ODBC 数据源管理器添加 DSN：
   - 64 位: `C:\Windows\System32\odbcad32.exe`
   - 32 位: `C:\Windows\SysWOW64\odbcad32.exe`

### 代码示例

```c
#include <stdio.h>
#include "sql.h"
#include "sqlext.h"

int main() {
    SQLHENV hEnv;
    SQLHDBC hDbc;
    SQLHSTMT hStmt;

    SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &hEnv);
    SQLSetEnvAttr(hEnv, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0);
    SQLAllocHandle(SQL_HANDLE_DBC, hEnv, &hDbc);
    SQLConnect(hDbc, (SQLCHAR*)"KingbaseES", SQL_NTS,
               (SQLCHAR*)"system", SQL_NTS, (SQLCHAR*)"123456", SQL_NTS);

    SQLAllocHandle(SQL_HANDLE_STMT, hDbc, &hStmt);

    // 执行查询
    SQLExecDirect(hStmt, (SQLCHAR*)"SELECT version()", SQL_NTS);

    SQLCHAR version[512];
    SQLBindCol(hStmt, 1, SQL_C_CHAR, version, sizeof(version), NULL);
    SQLFetch(hStmt);
    printf("Version: %s\n", version);

    SQLFreeHandle(SQL_HANDLE_STMT, hStmt);
    SQLDisconnect(hDbc);
    SQLFreeHandle(SQL_HANDLE_DBC, hDbc);
    SQLFreeHandle(SQL_HANDLE_ENV, hEnv);
    return 0;
}
```

### 编译

```bash
gcc test.c $(odbc_config --cflags) $(odbc_config --libs) -o test
```

---

## DCI (ESQL/C 嵌入式 SQL)

DCI 兼容 Oracle OCI 接口，适用于从 Oracle 迁移的 C 应用程序。

**库文件**：`libdcikdb.so`
**头文件**：`dci.h`、`dciapi.h`、`dcidef.h`、`dcitypes.h`

### 配置

创建 `sys_service.conf`：
```ini
[KingbaseES]
dbname=test
port=54321
host=127.0.0.1
AutoCommit=1
ClientEncoding=utf8
```

设置环境变量：`export KINGBASE_CONFDIR=/path/to/conf`

### 代码示例

```c
#include <stdio.h>
#include <string.h>
#include "dci.h"

int main() {
    DCIEnv *envhp = NULL;
    DCIError *errhp = NULL;
    DCISvcCtx *svchp = NULL;
    DCIStmt *stmthp = NULL;
    sword status;

    // 初始化环境
    DCIEnvCreate(&envhp, DCI_DEFAULT, NULL, NULL, NULL, NULL, 0, NULL);
    DCIHandleAlloc(envhp, (void **)&errhp, DCI_HTYPE_ERROR, 0, NULL);

    // 连接数据库
    DCILogon(envhp, errhp, &svchp,
        (text *)"SYSTEM", 6, (text *)"123456", 6,
        (text *)"KingbaseES", 10);

    // 创建语句句柄
    DCIHandleAlloc(envhp, (void **)&stmthp, DCI_HTYPE_STMT, 0, NULL);

    // 执行查询
    DCIStmtPrepare(stmthp, errhp, (text *)"SELECT version()", 16,
                   DCI_NTV_SYNTAX, DCI_DEFAULT);
    DCIStmtExecute(svchp, stmthp, errhp, 0, 0, NULL, NULL, DCI_DEFAULT);

    // 获取结果
    char version[512] = {0};
    DCIDefine *defnp = NULL;
    DCIDefineByPos(stmthp, &defnp, errhp, 1, version, sizeof(version),
                   SQLT_STR, NULL, NULL, NULL, DCI_DEFAULT);

    do {
        status = DCIStmtFetch(stmthp, errhp, 1, DCI_FETCH_NEXT, DCI_DEFAULT);
        if (status == DCI_SUCCESS) printf("Version: %s\n", version);
    } while (status == DCI_SUCCESS);

    // 清理
    DCIHandleFree(stmthp, DCI_HTYPE_STMT);
    DCILogoff(svchp, errhp);
    DCIHandleFree(svchp, DCI_HTYPE_SVCCTX);
    DCIHandleFree(errhp, DCI_HTYPE_ERROR);
    DCIHandleFree(envhp, DCI_HTYPE_ENV);
    return 0;
}
```

### 编译

```bash
gcc -I ./include -L ./lib test_dci.c -o testDci -ldcikdb -Wl,-rpath,./lib
```

---

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `无法加载 libkci.so.5` | 缺少符号链接 | `ln -s libkci.so libkci.so.5` |
| `ODBC 驱动找不到` | DSN 配置错误或注册表未更新 | 检查 odbc.ini / Windows 注册表 |
| `SSL 库冲突` | 系统 SSL 版本与驱动不兼容 | 联系技服获取静态依赖 SSL 的驱动包 |
| `VS Debug 模式崩溃` | Windows 驱动为 Release 版 | 使用 Release 模式编译 |
| `连接被拒绝` | 端口/地址错误或 sys_hba.conf 限制 | 检查端口（默认 54321）和认证配置 |

## 相关技能

- **kes-java** — JDBC 连接
- **kes-python** — ksycopg2 连接

## 参考文档

```
kes-c-odbc/
└── test-cases.md
```
