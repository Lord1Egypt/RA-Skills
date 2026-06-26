#!/usr/bin/env node
/**
 * InvoiceTW 統一發票查詢與管理指令
 * 台灣統一發票的核對、記錄與統計工具
 */

const fs = require('fs');
const path = require('path');

const LOTTERY_DIR = path.join(process.env.HOME || '/home/ckk', 'openclaw_workspace', 'InvoiceTW');
const RECEIPTS_FILE = path.join(LOTTERY_DIR, 'receipts.json');
const WINS_FILE = path.join(LOTTERY_DIR, 'wins.json');
const REPORTS_DIR = path.join(LOTTERY_DIR, 'reports');

// 初始化目錄結構
function init() {
    if (!fs.existsSync(LOTTERY_DIR)) {
        fs.mkdirSync(LOTTERY_DIR, { recursive: true });
    }
    if (!fs.existsSync(REPORTS_DIR)) {
        fs.mkdirSync(REPORTS_DIR, { recursive: true });
    }
    if (!fs.existsSync(RECEIPTS_FILE)) {
        fs.writeFileSync(RECEIPTS_FILE, JSON.stringify([], null, 2));
    }
    if (!fs.existsSync(WINS_FILE)) {
        fs.writeFileSync(WINS_FILE, JSON.stringify([], null, 2));
    }
}

// 加載發票記錄
function loadReceipts() {
    try {
        return JSON.parse(fs.readFileSync(RECEIPTS_FILE, 'utf8'));
    } catch (e) {
        return [];
    }
}

// 保存發票記錄
function saveReceipts(receipts) {
    fs.writeFileSync(RECEIPTS_FILE, JSON.stringify(receipts, null, 2));
}

// 加載中獎記錄
function loadWins() {
    try {
        return JSON.parse(fs.readFileSync(WINS_FILE, 'utf8'));
    } catch (e) {
        return [];
    }
}

// 保存中獎記錄
function saveWins(wins) {
    fs.writeFileSync(WINS_FILE, JSON.stringify(wins, null, 2));
}

// 查詢中獎號碼
function getWinningNumbers(month, year) {
    // 簡化的中獎號碼資料庫（實際應連接到財政部 API）
    // 這裡用隨機生成模擬
    return {
        '特獎': ['12345678', '87654321'],
        '一獎': ['11111111', '22222222', '33333333', '44444444', '55555555', 
                '66666666', '77777777', '88888888', '99999999', '00000000'],
        '二獎': ['11111112', '22222212', '33333312', '44444412', '55555512',
                '66666612', '77777712', '88888812', '99999912', '00000012',
                '11111121', '22222121', '33333121', '44444121', '55555121',
                '66666121', '77777121', '88888121', '99999121', '00000121'],
        '三獎': Array.from({length: 40}, (_, i) => `${10000000 + i}2`),
        '四獎': Array.from({length: 80}, (_, i) => `${20000000 + i}3`),
        '五獎': Array.from({length: 240}, (_, i) => `${30000000 + i}4`),
        '六獎': Array.from({length: 800}, (_, i) => `${40000000 + i}5`),
        '特別獎': ['12345670', '23456780', '34567890', '45678900', '56789000',
                  '67890000', '78900000', '89000000', '90000000', '00000001']
    };
}

// 核對發票是否中獎
function checkLottery(numbers) {
    const winning = getWinningNumbers('07', '2026');
    const results = [];
    
    for (const number of numbers) {
        const trimmed = number.trim();
        if (!/^\d{8}$/.test(trimmed)) {
            results.push({
                number: trimmed,
                valid: false,
                error: '發票號碼格式不正確（需為 8 位數字）'
            });
            continue;
        }
        
        let prize = null;
        let amount = 0;
        
        // 檢查特獎
        if (winning['特獎'].includes(trimmed)) {
            prize = '特獎';
            amount = 2000000;
        }
        // 檢查一獎
        else if (winning['一獎'].includes(trimmed)) {
            prize = '一獎';
            amount = 100000;
        }
        // 檢查二獎
        else if (winning['二獎'].includes(trimmed)) {
            prize = '二獎';
            amount = 20000;
        }
        // 檢查三獎
        else if (winning['三獎'].includes(trimmed)) {
            prize = '三獎';
            amount = 10000;
        }
        // 檢查四獎
        else if (winning['四獎'].includes(trimmed)) {
            prize = '四獎';
            amount = 4000;
        }
        // 檢查五獎
        else if (winning['五獎'].includes(trimmed)) {
            prize = '五獎';
            amount = 2000;
        }
        // 檢查六獎
        else if (winning['六獎'].includes(trimmed)) {
            prize = '六獎';
            amount = 400;
        }
        // 檢查特別獎
        else if (winning['特別獎'].includes(trimmed)) {
            prize = '特別獎';
            amount = 200;
        }
        
        results.push({
            number: trimmed,
            valid: true,
            prize: prize,
            amount: amount
        });
    }
    
    return results;
}

// 新增發票記錄
function addReceipt(args) {
    const receipts = loadReceipts();
    let number, date, store, amount, category, memo;
    
    // 解析參數格式：12345678 7/15 全家 50 元 民生用品
    const numberIndex = args.findIndex(arg => /^\d{8}$/.test(arg));
    if (numberIndex === -1) {
        return { success: false, error: '請提供有效的發票號碼（8 位數字）' };
    }
    
    number = args[numberIndex];
    date = args[numberIndex + 1] || new Date().toISOString().split('T')[0];
    store = args[numberIndex + 2] || '未知門市';
    
    // 金額可能是「50 元」或「50」
    let amountStr = args[numberIndex + 3] || '0';
    if (amountStr.endsWith('元')) {
        amountStr = amountStr.replace('元', '');
    }
    amount = parseInt(amountStr) || 0;
    
    // 分類可能是「元 民生用品」或「民生用品」
    let categoryStr = args[numberIndex + 4] || '其他';
    if (categoryStr.endsWith('元')) {
        categoryStr = categoryStr.replace('元', '').trim();
    }
    if (!categoryStr) {
        categoryStr = '其他';
    }
    category = categoryStr;
    
    memo = args[numberIndex + 5] || '';
    
    const newReceipt = {
        id: Date.now(),
        number: number,
        date: date,
        store: store,
        amount: amount,
        category: category,
        memo: memo,
        createdAt: new Date().toISOString()
    };
    
    receipts.push(newReceipt);
    saveReceipts(receipts);
    
    return {
        success: true,
        message: `已記錄發票 ${number}`,
        receipt: newReceipt
    };
}

// 列出發票
function listReceipts(filter = {}) {
    const receipts = loadReceipts();
    let filtered = receipts;
    
    if (filter.category) {
        filtered = filtered.filter(r => r.category === filter.category);
    }
    
    if (filter.month) {
        filtered = filtered.filter(r => r.date.startsWith(filter.month));
    }
    
    return filtered.reverse();
}

// 中獎統計
function calculateStats() {
    const receipts = loadReceipts();
    const wins = loadWins();
    
    const stats = {
        totalReceipts: receipts.length,
        totalAmount: receipts.reduce((sum, r) => sum + r.amount, 0),
        totalWon: wins.length,
        totalWinnings: wins.reduce((sum, w) => sum + w.amount, 0),
        byCategory: {},
        recentWins: wins.slice(-5)
    };
    
    // 按分類統計
    receipts.forEach(r => {
        if (!stats.byCategory[r.category]) {
            stats.byCategory[r.category] = { count: 0, amount: 0 };
        }
        stats.byCategory[r.category].count++;
        stats.byCategory[r.category].amount += r.amount;
    });
    
    return stats;
}

// 顯示報表
function showStats() {
    const stats = calculateStats();
    
    let output = '📊 統一發票統計報表\n\n';
    output += `📝 發票總數：${stats.totalReceipts} 張\n`;
    output += `💰 總金額：NT$${stats.totalAmount.toLocaleString()}\n`;
    output += `🎉 中獎次數：${stats.totalWon} 次\n`;
    output += `💵 中獎總額：NT$${stats.totalWinnings.toLocaleString()}\n\n`;
    
    output += '📁 按分類統計：\n';
    for (const [category, data] of Object.entries(stats.byCategory)) {
        output += `  ${category}: ${data.count} 張，NT$${data.amount.toLocaleString()}\n`;
    }
    
    if (stats.recentWins.length > 0) {
        output += '\n🏆 最近中獎記錄：\n';
        stats.recentWins.forEach(w => {
            output += `  - ${w.number}: ${w.prize} (NT$${w.amount})\n`;
        });
    }
    
    return output;
}

// 顯示中獎明細
function showWins() {
    const wins = loadWins();
    
    if (wins.length === 0) {
        return '🎊 目前沒有中獎記錄！恭喜，再接再厲！';
    }
    
    let output = '🏆 中獎發票明細:\n\n';
    wins.forEach(w => {
        output += `📋 發票 ${w.number}\n`;
        output += `   獎項：${w.prize}\n`;
        output += `   金額：NT$${w.amount.toLocaleString()}\n`;
        output += `   日期：${w.date}\n`;
        output += `   狀態：${w.claimed ? '✅ 已兌領' : '⏳ 未兌領'}\n\n`;
    });
    
    const pending = wins.filter(w => !w.claimed);
    if (pending.length > 0) {
        output += `⚠️ 尚有 ${pending.length} 張中獎發票未兌領\n`;
    }
    
    return output;
}

// 主指令處理
function main() {
    init();
    
    const args = process.argv.slice(2);
    const command = args[0];
    
    switch (command) {
        case 'check':
        case '核對':
            const numbers = args.slice(1).join(',').split(',').map(n => n.trim());
            const results = checkLottery(numbers);
            
            if (!results) {
                console.log('💡 使用方式：Invoice check 12345678,23456789');
                process.exit(0);
            }
            
            let output = '🔍 中獎查詢結果:\n\n';
            let hasWin = false;
            
            results.forEach(r => {
                if (!r.valid) {
                    output += `❌ ${r.number}: ${r.error}\n`;
                } else if (r.prize) {
                    output += `🎉 ${r.number}: **${r.prize}** - NT$${r.amount.toLocaleString()} ✨\n`;
                    hasWin = true;
                } else {
                    output += `⚪ ${r.number}: 未中獎\n`;
                }
            });
            
            if (hasWin) {
                output += '\n🎊 恭喜中獎！請攜帶發票和身份證到超商、郵局或財政部指定地點兌領。\n';
            } else {
                output += '\n😅 這次沒中獎，下次再接再厲！\n';
            }
            
            console.log(output);
            break;
            
        case 'add':
        case '新增':
        case '記':
            const idx = args.findIndex(a => /^\d{8}$/.test(a));
            if (idx === -1) {
                console.log('💡 使用方式：Invoice add 12345678 7/15 全家 50 元 民生用品');
                process.exit(0);
            }
            
            const newArgs = args.slice(1);
            const result = addReceipt(newArgs);
            
            if (result.success) {
                console.log(`✅ ${result.message}`);
                console.log(`   發票號碼：${result.receipt.number}`);
                console.log(`   日期：${result.receipt.date}`);
                console.log(`   門市：${result.receipt.store}`);
                console.log(`   金額：NT$${result.receipt.amount}`);
                console.log(`   分類：${result.receipt.category}`);
            } else {
                console.log(`❌ ${result.error}`);
            }
            break;
            
        case 'list':
        case '查詢':
        case '顯示':
            const filter = {};
            args.slice(1).forEach((arg, i) => {
                if (arg === '--category' && args[i + 1]) {
                    filter.category = args[i + 1];
                }
                if (arg === '--month' && args[i + 1]) {
                    filter.month = args[i + 1];
                }
            });
            
            const receipts = listReceipts(filter);
            
            if (receipts.length === 0) {
                console.log('📝 目前沒有發票記錄。');
            } else {
                console.log('📋 發票明細：\n');
                receipts.forEach(r => {
                    console.log(`📃 ${r.number}`);
                    console.log(`   日期：${r.date}`);
                    console.log(`   門市：${r.store}`);
                    console.log(`   金額：NT$${r.amount}`);
                    console.log(`   分類：${r.category}`);
                    if (r.memo) {
                        console.log(`   備註：${r.memo}`);
                    }
                    console.log();
                });
                console.log(`共 ${receipts.length} 張發票`);
            }
            break;
            
        case 'stats':
        case '統計':
        case '報表':
            console.log(showStats());
            break;
            
        case 'prizes':
        case '中獎':
        case 'wins':
            const prizeFilter = {};
            args.slice(1).forEach((arg, i) => {
                if (arg === '--pending') {
                    prizeFilter.pending = true;
                }
            });
            console.log(showWins(prizeFilter));
            break;
            
        case 'help':
        case '--help':
        case '-h':
            console.log(`
💡 InvoiceTW 統一發票查詢指令

使用方式：
  Invoice check <號碼>          核對發票中獎狀態
  Invoice add <號碼> <日期>     新增發票記錄
  Invoice list                  查詢所有發票
  Invoice stats                 統計報表
  Invoice prizes                中獎明細

範例：
  Invoice check 12345678,23456789
  Invoice add 12345678 7/15 全家 50 元 民生用品
  Invoice list --category 餐飲
  Invoice stats --category
  Invoice prizes --pending
`);
            break;
            
        default:
            console.log('💡 使用 Invoice help 查看說明');
            break;
    }
}

main();
