/**
 * Network Device Scanner - 局域网设备扫描器
 * 扫描局域网内活跃设备及其开放端口
 */

const { exec, spawn } = require('child_process');
const net = require('net');
const os = require('os');

const PORTS = [21, 22, 23, 53, 80, 135, 139, 443, 445, 554, 8000, 8080, 8443, 9000, 37777];
const TIMEOUT = 100; // 端口扫描超时(毫秒)

/**
 * 执行命令并返回输出
 */
function execCommand(cmd) {
    return new Promise((resolve, reject) => {
        exec(cmd, { timeout: 10000 }, (error, stdout, stderr) => {
            if (error && !stdout) {
                reject(error);
            } else {
                resolve(stdout);
            }
        });
    });
}

/**
 * 获取ARP表中的IP地址
 */
async function getArpTable() {
    const ips = new Set();
    try {
        const output = await execCommand('arp -a');
        const pattern = /172\.16\.10\.(\d+)\s+([0-9a-f]{2}-[0-9a-f]{2}-[0-9a-f]{2}-[0-9a-f]{2}-[0-9a-f]{2}-[0-9a-f]{2})/gi;
        let match;
        while ((match = pattern.exec(output)) !== null) {
            const mac = match[2].toLowerCase();
            if (mac !== 'ff-ff-ff-ff-ff-ff') {
                ips.add(`172.16.10.${match[1]}`);
            }
        }
    } catch (e) {
        console.error('ARP scan error:', e.message);
    }
    return Array.from(ips);
}

/**
 * 获取指定IP的MAC地址
 */
async function getMacForIp(ip) {
    try {
        const output = await execCommand(`arp -a ${ip}`);
        const pattern = /([0-9a-f]{2}-[0-9a-f]{2}-[0-9a-f]{2}-[0-9a-f]{2}-[0-9a-f]{2}-[0-9a-f]{2})/i;
        const match = output.match(pattern);
        return match ? match[1].toLowerCase() : '';
    } catch {
        return '';
    }
}

/**
 * 扫描单个端口
 */
function scanPort(ip, port) {
    return new Promise((resolve) => {
        const socket = new net.Socket();
        socket.setTimeout(TIMEOUT);
        
        socket.on('connect', () => {
            socket.destroy();
            resolve(port);
        });
        
        socket.on('timeout', () => {
            socket.destroy();
            resolve(null);
        });
        
        socket.on('error', () => {
            resolve(null);
        });
        
        socket.connect(port, ip);
    });
}

/**
 * 扫描IP的开放端口
 */
async function scanPorts(ip) {
    const results = await Promise.all(
        PORTS.map(port => scanPort(ip, port))
    );
    return results.filter(p => p !== null).sort((a, b) => a - b);
}

/**
 * 根据MAC前缀和开放端口识别设备类型
 */
function identifyDevice(mac, ports) {
    const macUpper = mac ? mac.toUpperCase() : '';
    const portStr = ports.join(',');
    
    // 端口识别规则
    if (portStr.includes('445') && portStr.includes('135')) {
        return 'Windows电脑 (SMB/远程管理)';
    }
    if (portStr.includes('22') && portStr.includes('80')) {
        return 'Linux服务器 (SSH/Web)';
    }
    if (portStr.includes('3389')) {
        return 'Windows电脑 (RDP)';
    }
    if (portStr.includes('554') || portStr.includes('37777')) {
        return '监控摄像头 (RTSP)';
    }
    if (portStr.includes('8000')) {
        return 'Web服务器';
    }
    if (portStr.includes('80') || portStr.includes('8080') || portStr.includes('443') || portStr.includes('8443')) {
        return 'Web服务器/设备';
    }
    
    // MAC前缀识别规则
    if (!macUpper) return '未知设备';
    
    const macPrefixes = {
        'E4-68-A3': '小米路由器',
        '40-31-3C': '小米设备 (智能电视/IoT)',
        '00-1D-0C': '小米设备',
        'DC-2E-97': '小米设备',
        '30-9C-23': 'Windows电脑',
        '24-DF-6A': 'Windows电脑',
        '00-1E-58': 'Dell设备',
        '00-25-9E': 'Dell设备',
        '00-FF-EE': 'Dell设备',
        'AC-DC-0E': 'Dell设备',
        'F8-E4-3B': 'Dell电脑',
        '00-14-22': 'Dell电脑',
        '00-1B-21': 'Intel设备',
        '00-0C-29': 'VMware虚拟机',
        '00-50-56': 'VMware虚拟机',
        '00-1C-14': 'VMware虚拟机',
    };
    
    // 精确匹配
    if (macPrefixes[macUpper]) {
        return macPrefixes[macUpper];
    }
    
    // 前缀匹配
    for (const [prefix, device] of Object.entries(macPrefixes)) {
        if (prefix.endsWith('-')) {
            if (macUpper.startsWith(prefix.slice(0, -1))) {
                return device;
            }
        } else if (macUpper.startsWith(prefix)) {
            return device;
        }
    }
    
    return '未知设备';
}

/**
 * 解析IP为数字用于排序
 */
function ipToNumber(ip) {
    const parts = ip.split('.');
    return parseInt(parts[0]) * 16777216 + parseInt(parts[1]) * 65536 + parseInt(parts[2]) * 256 + parseInt(parts[3]);
}

/**
 * 主函数
 */
async function main() {
    console.log('Scanning...');
    
    // 从ARP表获取已知IP
    let knownIps = await getArpTable();
    
    // 额外扫描一些常见IP
    const additionalIps = ['172.16.10.234'];
    for (const ip of additionalIps) {
        if (!knownIps.includes(ip)) {
            knownIps.push(ip);
        }
    }
    
    // 去重
    knownIps = [...new Set(knownIps)];
    console.log(`Found IPs: ${knownIps.join(', ')}`);
    
    const results = [];
    
    // 扫描每个IP的端口
    for (const ip of knownIps) {
        const openPorts = await scanPorts(ip);
        
        if (openPorts.length > 0) {
            const mac = await getMacForIp(ip);
            const deviceType = identifyDevice(mac, openPorts);
            
            results.push({
                ip,
                mac,
                ports: openPorts,
                deviceType
            });
        }
    }
    
    // 按IP排序
    results.sort((a, b) => ipToNumber(a.ip) - ipToNumber(b.ip));
    
    // 输出格式: IP|MAC|Ports|DeviceType
    for (const device of results) {
        console.log(`${device.ip}|${device.mac}|${device.ports.join(',')}|${device.deviceType}`);
    }
}

main().catch(console.error);
