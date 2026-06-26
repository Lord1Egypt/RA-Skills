const fs = require('fs');
const path = require('path');
const OKXClient = require('../lib/okx-client');

function getConfig() {
    const configPath = '/root/.openclaw/workspace/okx_data/config.json';
    if (fs.existsSync(configPath)) {
        return JSON.parse(fs.readFileSync(configPath, 'utf8'));
    }
    return {
        apiKey: process.env.OKX_API_KEY,
        secretKey: process.env.OKX_SECRET_KEY,
        passphrase: process.env.OKX_PASSPHRASE,
        isSimulation: process.env.OKX_IS_SIMULATION === 'true'
    };
}

function getGridSettings() {
    const settingsPath = '/root/.openclaw/workspace/okx_data/grid_settings.json';
    if (fs.existsSync(settingsPath)) {
        return JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
    }
    return {};
}

async function runReport() {
    try {
        const client = new OKXClient(getConfig());
        const settings = getGridSettings();

        // Collect unique instIds from settings
        const instIds = [...new Set(Object.values(settings).map(s => s.instId))];

        // Fetch fills and pending orders for all instruments
        const allFills = [];
        const allPending = [];
        await Promise.all(instIds.map(async (instId) => {
            const [fills, pending] = await Promise.all([
                client.request('/trade/fills', 'GET', { instId }),
                client.request('/trade/orders-pending', 'GET', { instId })
            ]);
            if (Array.isArray(fills)) allFills.push(...fills.map(f => ({ ...f, _instId: instId })));
            if (Array.isArray(pending)) allPending.push(...pending.map(o => ({ ...o, _instId: instId })));
        }));

        const oneHourAgo = Date.now() - (60 * 60 * 1000);
        const recentFills = allFills.filter(f => parseInt(f.ts) > oneHourAgo);

        // Build stats per grid type from settings
        const gridTypes = {};
        for (const [key, cfg] of Object.entries(settings)) {
            gridTypes[key] = {
                instId: cfg.instId,
                sizePerGrid: cfg.sizePerGrid,
                label: key,
                buyUsdt: 0, buyQty: 0, buyCount: 0,
                sellUsdt: 0, sellQty: 0, sellCount: 0
            };
        }

        recentFills.forEach(f => {
            const px = parseFloat(f.fillPx || 0);
            const sz = parseFloat(f.fillSz || 0);
            const instId = f._instId || f.instId;

            // Match to grid type by instId and size
            let matched = null;
            for (const [key, gt] of Object.entries(gridTypes)) {
                if (gt.instId === instId && Math.abs(sz - gt.sizePerGrid) < gt.sizePerGrid * 0.5) {
                    matched = key;
                    break;
                }
            }
            if (!matched) return;

            const s = gridTypes[matched];
            if (f.side === 'buy') {
                s.buyUsdt += px * sz; s.buyQty += sz; s.buyCount++;
            } else {
                s.sellUsdt += px * sz; s.sellQty += sz; s.sellCount++;
            }
        });

        const formatStats = (s) => {
            const avgB = s.buyQty > 0 ? (s.buyUsdt / s.buyQty).toFixed(2) : '0.00';
            const avgS = s.sellQty > 0 ? (s.sellUsdt / s.sellQty).toFixed(2) : '0.00';
            return `  - 成交: ${s.buyCount + s.sellCount} 笔 (买 ${s.buyCount} / 卖 ${s.sellCount})\n  - 均价: 买 ${avgB} / 卖 ${avgS}\n  - 总额: 买 ${s.buyUsdt.toFixed(2)} / 卖 ${s.sellUsdt.toFixed(2)} USDT`;
        };

        const gridLabels = {
            main: '🐋 **大网格 BTC (0.002 BTC)**',
            micro: '🌀 **小网格 BTC (0.0003 BTC)**',
            eth_micro: '💎 **小网格 ETH (0.01 ETH)**'
        };

        const now = new Date();
        const timeStr = now.toISOString().replace('T', ' ').substring(0, 19);

        let output = `📊 **OKX 网格策略报表 (${timeStr} UTC)**\n\n`;

        // Output stats per grid
        for (const [key, s] of Object.entries(gridTypes)) {
            const label = gridLabels[key] || `📌 **${key} (${s.instId})**`;
            output += `${label}\n${formatStats(s)}\n\n`;
        }

        // Pending orders grouped by instId
        for (const instId of instIds) {
            const pending = allPending.filter(o => o._instId === instId);
            const buyOrders = pending.filter(o => o.side === 'buy').sort((a, b) => parseFloat(b.px) - parseFloat(a.px));
            const sellOrders = pending.filter(o => o.side === 'sell').sort((a, b) => parseFloat(a.px) - parseFloat(b.px));

            output += `📝 **${instId} 挂单 (${pending.length} 笔):**\n`;
            output += `📈 *卖单 (Top 3):* ${sellOrders.slice(0, 3).map(o => `${parseFloat(o.px).toFixed(0)}(${o.sz})`).join(', ')}\n`;
            output += `📉 *买单 (Top 3):* ${buyOrders.slice(0, 3).map(o => `${parseFloat(o.px).toFixed(0)}(${o.sz})`).join(', ')}\n\n`;
        }

        output += `(注: OKX-Trader Skill 自动生成)`;
        console.log(output);
    } catch (e) {
        console.error('Error:', e.message);
    }
}

runReport();
