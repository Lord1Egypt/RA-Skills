/**
 * 命令安全验证
 * 
 * 验证命令是否在允许的白名单中，防止执行危险命令
 */

/**
 * 允许的命令白名单（正则表达式）
 * 
 * 这些命令被认为是安全的，可以执行
 */
const ALLOWED_COMMANDS = [
  // 系统信息
  /^uptime$/,
  /^free\s*(-h)?$/,
  /^df\s*(-h)?$/,
  /^df\s+-h\s+\/$/,
  /^top\s+-b\s+-n\s+1$/,
  /^ps\s+aux$/,
  /^ps\s+ef$/,
  /^uname\s+(-a)?$/,
  /^hostname$/,
  /^whoami$/,
  /^id$/,

  // 日志查看
  /^tail\s+(-n\s+\d+)?\s+.*$/,
  /^tail\s+(-n\s+\d+)?\s+.*\.log\s*\|\s*grep\s+.*$/,
  /^grep\s+.*\s+.*$/,
  /^cat\s+.*\.log$/,
  /^less\s+.*\.log$/,
  /^journalctl\s+.*$/,

  // 网络检查
  /^netstat\s+(-tulpn)?$/,
  /^ss\s+(-tulpn)?$/,
  /^lsof\s+-i:\d+$/,
  /^curl\s+-I\s+.*$/,
  /^wget\s+.*$/,
  /^ping\s+-c\s+\d+\s+.*$/,

  // 进程管理（只读）
  /^systemctl\s+status\s+.*$/,
  /^systemctl\s+is-active\s+.*$/,
  /^service\s+.*\s+status$/,

  // 磁盘和文件（只读）
  /^ls\s+(-la)?$/,
  /^ls\s+(-la)?\s+.*$/,
  /^du\s+-sh\s+.*$/,
  /^find\s+.*$/,
  /^stat\s+.*$/,

  // 端口检查
  /^nc\s+-zv\s+.*$/,
  /^telnet\s+.*$/,

  // 安全检查
  /^last\s+(-n\s+\d+)?$/,
  /^w$/,
  /^who$/,

  // Docker（只读）
  /^docker\s+ps$/,
  /^docker\s+ps\s+-a$/,
  /^docker\s+images$/,
  /^docker\s+inspect\s+.*$/,
  /^docker\s+logs\s+.*$/,
  /^docker\s+stats\s+.*$/,

  // Kubernetes（只读）
  /^kubectl\s+get\s+.*$/,
  /^kubectl\s+describe\s+.*$/,
  /^kubectl\s+logs\s+.*$/,
  /^kubectl\s+top\s+.*$/,

  // 其他安全命令
  /^date$/,
  /^timedatectl\s+status$/,
  /^env$/,
  /^echo\s+.*$/,
  /^cat\s+.*$/,
  /^head\s+.*$/,
  /^tail\s+.*$/,
]

/**
 * 危险命令黑名单（正则表达式）
 * 
 * 这些命令绝对不允许执行
 */
const DANGEROUS_COMMANDS = [
  // 文件删除
  /^rm\s+.*$/,
  /^rmdir\s+.*$/,

  // 文件修改
  /^mv\s+.*$/,
  /^cp\s+.*$/,
  /^touch\s+.*$/,
  /^chmod\s+.*$/,
  /^chown\s+.*$/,

  // 系统控制
  /^shutdown\s+.*$/,
  /^reboot\s+.*$/,
  /^poweroff\s+.*$/,
  /^halt\s+.*$/,

  // 用户管理
  /^useradd\s+.*$/,
  /^userdel\s+.*$/,
  /^usermod\s+.*$/,
  /^passwd\s+.*$/,

  // 包管理
  /^apt-get\s+.*$/,
  /^apt\s+.*$/,
  /^yum\s+.*$/,
  /^dnf\s+.*$/,
  /^pacman\s+.*$/,
  /^npm\s+.*$/,
  /^pip\s+.*$/,

  // 服务控制
  /^systemctl\s+(start|stop|restart|reload)\s+.*$/,
  /^service\s+.*\s+(start|stop|restart|reload)$/,

  // 防火墙
  /^iptables\s+.*$/,
  /^ufw\s+.*$/,
  /^firewall-cmd\s+.*$/,

  // 网络配置
  /^ifconfig\s+.*$/,
  /^ip\s+.*$/,
  /^route\s+.*$/,

  // Shell命令
  /^:.*$/,
  /^&&.*$/,
  /^\|\|.*$/,
  /^;.*$/,
  />\s*.*$/,
  />>\s*.*$/,

  // 下载和执行
  /curl.*\|\s*(bash|sh|python|perl|ruby)/,
  /wget.*\|\s*(bash|sh|python|perl|ruby)/,

  // 反弹shell
  /bash\s+-i\s+>&/,
  /nc\s+.*\s+-e/,

  // 其他危险命令
  /^dd\s+.*$/,
  /^mkfs\s+.*$/,
  /^fdisk\s+.*$/,
  /^parted\s+.*$/,
]

/**
 * 验证命令是否安全
 * 
 * @param command 要验证的命令
 * @returns 验证结果和错误信息
 */
export function validateCommand(command: string): { safe: boolean; reason?: string } {
 const trimmedCommand = command.trim()

 // 检查是否为空
 if (!trimmedCommand) {
 return { safe: false, reason: '命令不能为空' }
 }

 // 检查是否包含注释字符（可能隐藏恶意命令）
 if (trimmedCommand.includes('#')) {
 return { safe: false, reason: '命令包含注释字符，可能绕过安全检查' }
 }

 // 检查是否包含管道和重定向（可能绕过白名单）
 if (trimmedCommand.includes('|') || trimmedCommand.includes('>') || trimmedCommand.includes('<')) {
 return { safe: false, reason: '命令包含管道或重定向，可能绕过安全检查' }
 }

 // 检查是否包含命令替换
 if (trimmedCommand.includes('$(') || trimmedCommand.includes('`')) {
 return { safe: false, reason: '命令包含命令替换，可能绕过安全检查' }
 }

 // 检查是否包含分号（可能执行多个命令）
 if (trimmedCommand.includes(';')) {
 return { safe: false, reason: '命令包含分号，可能执行多个命令' }
 }

 // 检查是否包含&&或||
 if (trimmedCommand.includes('&&') || trimmedCommand.includes('||')) {
 return { safe: false, reason: '命令包含逻辑运算符，可能执行多个命令' }
 }

 // 检查危险命令
 for (const pattern of DANGEROUS_COMMANDS) {
 if (pattern.test(trimmedCommand)) {
 return { safe: false, reason: `命令包含危险操作: ${trimmedCommand}` }
 }
 }

 // 检查是否在白名单中
 for (const pattern of ALLOWED_COMMANDS) {
 if (pattern.test(trimmedCommand)) {
 return { safe: true }
 }
 }

 // 不在白名单中，拒绝执行
 return { safe: false, reason: `命令不在允许的白名单中: ${trimmedCommand}` }
}

/**
 * 批量验证命令
 * 
 * @param commands 要验证的命令列表
 * @returns 验证结果
 */
export function validateCommands(commands: string[]): { safe: boolean; invalid: string[] } {
  const invalid: string[] = []

  for (const command of commands) {
    const result = validateCommand(command)
    if (!result.safe) {
      invalid.push(command)
    }
  }

  return { safe: invalid.length === 0, invalid }
}

/**
 * 获取允许的命令列表（用于文档）
 */
export function getAllowedCommandsList(): string[] {
  return ALLOWED_COMMANDS.map(pattern => pattern.toString())
}

/**
 * 获取危险命令列表（用于文档）
 */
export function getDangerousCommandsList(): string[] {
  return DANGEROUS_COMMANDS.map(pattern => pattern.toString())
}
