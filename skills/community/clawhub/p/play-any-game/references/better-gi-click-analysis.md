# BetterGI 点击实现技术分析

## 概述

BetterGI 使用了两种点击方式：
1. **前台点击**：使用 `SendInput` API 模拟真实鼠标操作
2. **后台点击**：使用 `PostMessage` 发送窗口消息

## 核心架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        坐标系统层级                              │
├─────────────────────────────────────────────────────────────────┤
│  Level 0: 桌面坐标 (Desktop)                                    │
│     ↓                                                           │
│  Level 1: 游戏捕获区域 (GameCaptureArea)                        │
│     ↓                                                           │
│  Level 2: 窗口内矩形区域 (Part)                                 │
│     ↓                                                           │
│  Level 3: 识别到的图像区域 (DetectedArea)                       │
└─────────────────────────────────────────────────────────────────┘
```

## 一、窗口位置获取

### 1.1 获取窗口真实边界

```csharp
// SystemControl.cs
public static RECT GetWindowRect(nint hWnd)
{
    // 使用 DwmGetWindowAttribute 获取窗口真实边界
    // 不包括 Windows DWM 添加的阴影等效果
    DwmApi.DwmGetWindowAttribute<RECT>(hWnd, 
        DwmApi.DWMWINDOWATTRIBUTE.DWMWA_EXTENDED_FRAME_BOUNDS, 
        out var windowRect);
    return windowRect;
}
```

### 1.2 获取客户区大小

```csharp
// SystemControl.cs
public static RECT GetGameScreenRect(nint hWnd)
{
    User32.GetClientRect(hWnd, out var clientRect);
    return clientRect;
}
```

### 1.3 计算捕获区域

```csharp
// SystemControl.cs
public static RECT GetCaptureRect(nint hWnd)
{
    var windowRect = GetWindowRect(hWnd);      // 窗口边界
    var gameScreenRect = GetGameScreenRect(hWnd); // 客户区
    
    // 计算客户区在屏幕上的位置
    var left = windowRect.Left;
    var top = windowRect.Top + windowRect.Height - gameScreenRect.Height;
    var right = left + gameScreenRect.Width;
    var bottom = top + gameScreenRect.Height;
    
    return new RECT(left, top, right, bottom);
}
```

## 二、屏幕分辨率获取

### 2.1 使用 GetDeviceCaps（关键！）

```csharp
// PrimaryScreen.cs
public static Size WorkingArea
{
    get
    {
        var hdc = User32.GetDC(IntPtr.Zero);
        var size = new Size
        {
            Width = Gdi32.GetDeviceCaps(hdc, DeviceCap.HORZRES),
            Height = Gdi32.GetDeviceCaps(hdc, DeviceCap.VERTRES)
        };
        User32.ReleaseDC(IntPtr.Zero, hdc);
        return size;
    }
}
```

**重要区别**：
- `GetDeviceCaps(HORZRES/VERTRES)` 返回的是**物理分辨率**（无 DPI 缩放）
- `GetSystemMetrics(SM_CXSCREEN/SM_CYSCREEN)` 返回的是**逻辑分辨率**（有 DPI 缩放）
- 在 125% DPI 缩放下，物理 1920x1080 显示为逻辑 1536x864

## 三、前台点击实现

### 3.1 使用 SendInput API

BetterGI 使用 `SendInput` API 而不是 `mouse_event`：

```csharp
// MouseSimulator.cs
public IMouseSimulator MoveMouseTo(double absoluteX, double absoluteY)
{
    User32.INPUT[] inputList = new InputBuilder()
        .AddAbsoluteMouseMovement((int)Math.Truncate(absoluteX), (int)Math.Truncate(absoluteY))
        .ToArray();
    SendSimulatedInput(inputList);
    return this;
}
```

### 3.2 坐标归一化公式

```csharp
// DesktopRegion.cs
public static void DesktopRegionClick(double cx, double cy)
{
    Simulation.SendInput.Mouse.MoveMouseTo(
        cx * 65535 * 1d / PrimaryScreen.WorkingArea.Width,
        cy * 65535 * 1d / PrimaryScreen.WorkingArea.Height
    ).LeftButtonDown().Sleep(50).LeftButtonUp().Sleep(50);
}
```

**公式**：
```
normalizedX = screenX * 65535 / physicalScreenWidth
normalizedY = screenY * 65535 / physicalScreenHeight
```

### 3.3 点击流程

```csharp
// ClickExtension.cs
public static void Click(this Point point)
{
    Simulation.SendInput.Mouse
        .MoveMouseTo(
            point.X * 65535 * 1d / PrimaryScreen.WorkingArea.Width,
            point.Y * 65535 * 1d / PrimaryScreen.WorkingArea.Height
        )
        .LeftButtonDown()
        .Sleep(50)
        .LeftButtonUp();
}
```

## 四、后台点击实现

### 4.1 PostMessage 方式

```csharp
// PostMessageSimulator.cs
public PostMessageSimulator LeftButtonClickBackground(int x, int y)
{
    // 1. 激活窗口
    User32.PostMessage(_hWnd, User32.WindowMessage.WM_ACTIVATE, 1, 0);
    
    // 2. 构造 LPARAM
    var p = MakeLParam(x, y);
    
    // 3. 发送点击消息
    User32.PostMessage(_hWnd, WM_LBUTTONDOWN, 1, p);
    Thread.Sleep(100);
    User32.PostMessage(_hWnd, WM_LBUTTONUP, 0, p);
    
    return this;
}

public static int MakeLParam(int x, int y) => (y << 16) | (x & 0xFFFF);
```

## 五、坐标转换流程

### 5.1 从游戏坐标到桌面坐标

```csharp
// GameCaptureRegion.cs
public static void GameRegionClick(Func<Size, double, (double, double)> posFunc)
{
    var captureAreaRect = TaskContext.Instance().SystemInfo.CaptureAreaRect;
    var assetScale = TaskContext.Instance().SystemInfo.ScaleTo1080PRatio;
    
    // 1. 计算游戏内坐标
    var (cx, cy) = posFunc(new Size(captureAreaRect.Width, captureAreaRect.Height), assetScale);
    
    // 2. 转换到桌面坐标并点击
    DesktopRegion.DesktopRegionClick(captureAreaRect.X + cx, captureAreaRect.Y + cy);
}
```

### 5.2 1080P 坐标转换

```csharp
// GameCaptureRegion.cs
public static void GameRegion1080PPosClick(double cx, double cy)
{
    // 1080P坐标转换到实际游戏窗口坐标
    GameRegionClick((_, scale) => (cx * scale, cy * scale));
}
```

## 六、关键代码路径

```
用户点击请求
    ↓
GameCaptureRegion.GameRegionClick()
    ↓
计算桌面坐标 = CaptureAreaRect.Position + 游戏内坐标
    ↓
DesktopRegion.DesktopRegionClick(桌面坐标)
    ↓
Simulation.SendInput.Mouse.MoveMouseTo(归一化坐标)
    ↓
SendInput API 执行点击
```

## 七、Python 实现要点

### 7.1 获取物理屏幕分辨率

```python
import ctypes

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

def get_physical_screen_size():
    """获取物理屏幕分辨率（无 DPI 缩放）"""
    hdc = user32.GetDC(0)
    width = gdi32.GetDeviceCaps(hdc, 8)   # HORZRES = 8
    height = gdi32.GetDeviceCaps(hdc, 10) # VERTRES = 10
    user32.ReleaseDC(0, hdc)
    return width, height
```

### 7.2 使用 SendInput API

```python
import ctypes
from ctypes import wintypes

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ('dx', wintypes.LONG),
        ('dy', wintypes.LONG),
        ('mouseData', wintypes.DWORD),
        ('dwFlags', wintypes.DWORD),
        ('time', wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(wintypes.ULONG)),
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ('type', wintypes.DWORD),
        ('mi', MOUSEINPUT),
        ('padding', ctypes.c_ubyte * 8),  # padding for union
    ]

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

def click_sendinput(x, y, screen_width, screen_height):
    """使用 SendInput API 点击"""
    normalized_x = int(x * 65535 / screen_width)
    normalized_y = int(y * 65535 / screen_height)
    
    inputs = (INPUT * 3)()
    
    # 移动鼠标
    inputs[0].type = INPUT_MOUSE
    inputs[0].mi.dx = normalized_x
    inputs[0].mi.dy = normalized_y
    inputs[0].mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
    
    # 左键按下
    inputs[1].type = INPUT_MOUSE
    inputs[1].mi.dwFlags = MOUSEEVENTF_LEFTDOWN
    
    # 左键释放
    inputs[2].type = INPUT_MOUSE
    inputs[2].mi.dwFlags = MOUSEEVENTF_LEFTUP
    
    user32.SendInput(3, ctypes.byref(inputs), ctypes.sizeof(INPUT))
```

## 八、常见问题

### 8.1 点击位置偏移

**原因**：使用了逻辑分辨率而不是物理分辨率

**解决**：使用 `GetDeviceCaps` 获取物理分辨率

### 8.2 DPI 缩放问题

**原因**：Windows DPI 缩放导致坐标计算错误

**解决**：
1. 使用 `GetDeviceCaps` 获取物理分辨率
2. 或在程序启动时设置 DPI 感知

### 8.3 窗口边框问题

**原因**：`GetWindowRect` 包含窗口边框和阴影

**解决**：使用 `DwmGetWindowAttribute` 获取真实边界

## 九、总结

BetterGI 点击实现的核心要点：

1. **坐标系统**：使用桌面坐标系，所有坐标最终转换到桌面坐标
2. **分辨率获取**：使用 `GetDeviceCaps` 获取物理分辨率
3. **窗口位置**：使用 `DwmGetWindowAttribute` 获取真实边界
4. **点击 API**：使用 `SendInput` 而不是 `mouse_event`
5. **坐标归一化**：`x * 65535 / screenWidth`
