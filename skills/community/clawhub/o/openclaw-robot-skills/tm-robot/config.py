"""
TM Robot Skill - 配置文件
⚠️ 请根据实际机器人 IP 修改以下配置
"""

# ==================== 机器人连接配置 ====================

# TM5 机器人 IP 地址
# 查看方式: TMflow -> Robot Setting -> Network -> IP Address
ROBOT_IP = "192.168.1.13"

# 连接超时时间（秒）
CONNECT_TIMEOUT = 5.0

# ==================== 运动参数 ====================

# 默认速度 (0-1, 0.1 = 10%)
DEFAULT_SPEED = 0.1

# 默认加速度 (0-100, 50 = 50%)
DEFAULT_ACCEL = 50

# 直线运动速度 (mm/s)
DEFAULT_LINE_SPEED = 50

# ==================== SVR 变量名称 ====================

# TMflow 标准变量名（通常不需要修改）
VARIABLE_NAMES = {
    "joint_angle": "Joint_Angle",      # 关节角度
    "joint_target": "Joint_Target",    # 目标关节
    "pos_actual": "Pos_Actual",       # 实际位置
    "pos_target": "Pos_Target",       # 目标位置
    "cartesian_actual": "Cartesian_Actual",  # 笛卡尔位置
    "robot_mode": "RobotMode",        # 机器人模式
    "error_code": "RobotErrCode",     # 错误码
    "project_name": "ProjectName",    # 当前项目
}

# ==================== I/O 引脚配置 ====================

# 数字输入引脚
DI_START = 0   # 开始信号
DI_STOP = 1    # 停止信号
DI_HOME = 2    # 回零信号

# 数字输出引脚
DO_READY = 0   # 就绪信号
DO_RUNNING = 1 # 运行中信号
DO_ERROR = 2   # 错误信号
DO_GRIPPER = 10 # 夹爪控制

# ==================== 安全限制 ====================

# 最大关节角度限制（度）
JOINT_LIMITS = {
    "j1": (-180, 180),
    "j2": (-130, 130),
    "j3": (-150, 150),
    "j4": (-180, 180),
    "j5": (-180, 180),
    "j6": (-360, 360),  # J6 通常无限制
}

# 工作空间边界（mm）
WORKSPACE_LIMITS = {
    "x": (-850, 850),
    "y": (-850, 850),
    "z": (-500, 1200),
}

# ==================== 日志配置 ====================

# 是否打印详细日志
VERBOSE = True

# 日志文件路径（空字符串表示不写入文件）
LOG_FILE = ""
