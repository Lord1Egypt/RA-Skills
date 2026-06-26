/* ========= Polymarket 交易终端 - 前端逻辑 ========= */

const dashboardState = {
    accountMode: 'paper',
    tradingEnabled: true,
    togglePending: false,
    controlError: '',
    paperBalance: null,
    realBalance: null,
    config: null,
    aiHistory: [],
    decisionSignal: null,
    positionCounts: { paper: 0, real: 0 },
    expandedPositionId: null,
};

try {
    const savedMode = window.localStorage.getItem('polymarket_account_mode');
    if (savedMode === 'real' || savedMode === 'paper') {
        dashboardState.accountMode = savedMode;
    }
} catch (e) {
    // ignore localStorage issues
}

function setText(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
}

function escapeHtml(value) {
    return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function formatUSD(n) {
    if (n === null || n === undefined || isNaN(n)) return '--';
    return '$' + Number(n).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function formatSignedUSD(n) {
    if (n === null || n === undefined || isNaN(n)) return '--';
    const value = Number(n);
    return `${value >= 0 ? '+' : ''}$${value.toFixed(2)}`;
}

function shortTime(iso) {
    if (!iso) return '--';
    try {
        const d = new Date(iso);
        return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    } catch {
        return iso;
    }
}

function shortMinute(iso) {
    if (!iso) return '--';
    try {
        const d = new Date(iso);
        return d.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    } catch {
        return iso;
    }
}

function shortWallet(address) {
    if (!address || typeof address !== 'string') return '--';
    if (address.length < 12) return address;
    return address.slice(0, 6) + '...' + address.slice(-4);
}

function toNumber(value) {
    if (value === null || value === undefined || value === '') return null;
    const num = Number(value);
    return isNaN(num) ? null : num;
}

function firstValue(...values) {
    for (const value of values) {
        if (value !== null && value !== undefined && value !== '') return value;
    }
    return null;
}

function firstNumber(...values) {
    for (const value of values) {
        const num = toNumber(value);
        if (num !== null) return num;
    }
    return null;
}

function extractPnlFromText(text) {
    if (!text || typeof text !== 'string') return null;
    const match = text.match(/实现盈亏\s*([+-]?\d+(?:\.\d+)?)/);
    if (!match) return null;
    return toNumber(match[1]);
}

function getBalanceSourceLabel(source) {
    const sourceMap = {
        polygon_rpc: 'Polygon RPC',
        etherscan_v2: 'Etherscan',
        paper_live: 'Paper Account',
    };
    return sourceMap[source] || '链上接口';
}

function getActiveAccountMode() {
    return dashboardState.accountMode === 'real' ? 'real' : 'paper';
}

function getEmptyTradeMessage() {
    return getActiveAccountMode() === 'real' ? '暂无真实成交记录' : '暂无模拟交易记录';
}

function getEmptyPositionMessage() {
    return getActiveAccountMode() === 'real' ? '暂无真实持仓' : '暂无模拟持仓';
}

function getTradeColspan() {
    return 7;
}

function setOutcomeLabels(left, right) {
    setText('outcome-yes-label', left || 'YES');
    setText('outcome-no-label', right || 'NO');
}

function setMarketDominance(leftValue, rightValue) {
    const leftCard = document.getElementById('prob-yes-card');
    const rightCard = document.getElementById('prob-no-card');
    if (!leftCard || !rightCard) return;
    leftCard.classList.remove('is-dominant');
    rightCard.classList.remove('is-dominant');
    if (leftValue > rightValue) leftCard.classList.add('is-dominant');
    else if (rightValue > leftValue) rightCard.classList.add('is-dominant');
}

function renderAccountMode() {
    const isReal = getActiveAccountMode() === 'real';
    const metricsRow = document.getElementById('metrics-row');
    const paperBtn = document.getElementById('switch-paper');
    const realBtn = document.getElementById('switch-real');
    const badge = document.getElementById('view-badge');
    const caption = document.getElementById('control-caption');
    const paperCard = document.getElementById('paper-balance-card');
    const assetCard = document.getElementById('asset-change-card');
    const realCard = document.getElementById('real-balance-card');

    if (paperBtn) paperBtn.classList.toggle('active', !isReal);
    if (realBtn) realBtn.classList.toggle('active', isReal);
    if (paperCard) {
        paperCard.classList.toggle('is-selected', !isReal);
        paperCard.classList.toggle('is-hidden', isReal);
    }
    if (assetCard) {
        assetCard.classList.toggle('is-hidden', isReal);
    }
    if (realCard) {
        realCard.classList.toggle('is-selected', isReal);
        realCard.classList.toggle('is-hidden', !isReal);
    }
    if (metricsRow) {
        metricsRow.style.setProperty('--metric-columns', isReal ? '3' : '4');
    }

    if (badge) {
        badge.textContent = isReal ? '真实账户视图' : '模拟账户视图';
    }

    if (caption) {
        caption.textContent = isReal
            ? '真实账户视图只读取真实余额、公开持仓和公开成交，不会触发真实下单。'
            : '模拟账户视图展示本地 100U 纸上交易记录与持仓。';
    }

    setText('trade-panel-title', isReal ? '最近真实成交' : '全部模拟交易流水');
    setText(
        'trade-panel-caption',
        isReal
            ? '读取 Polymarket 公开成交记录；这里只读展示，不会发真实订单。'
            : '完整展示这轮测试的全部交易记录，包含开仓、平仓、盈利/亏损和每一步的操作说明。'
    );
    setText('position-panel-title', isReal ? '当前真实持仓' : '当前模拟持仓');
    setText(
        'position-panel-caption',
        isReal
            ? '读取 Polymarket 公开持仓；如果为空，说明当前没有公开可见的持仓。'
            : '每个盘口 1U；默认只看摘要，点开后再看入场 ask、当前 bid、点差和到期时间。'
    );
    renderPaperPerformance();
}

function renderPaperPerformance() {
    const card = document.getElementById('asset-change-card');
    const valueEl = document.getElementById('asset-change-value');
    const subEl = document.getElementById('asset-change-sub');
    if (!card || !valueEl || !subEl) return;

    const cfg = dashboardState.config || {};
    const paperSummary = dashboardState.paperBalance || {};
    const startBalance = firstNumber(cfg.paper_start_balance, 100);
    const endingBalance = firstNumber(cfg.paper_balance, paperSummary.balance);
    let pnl = firstNumber(cfg.paper_profit);
    if (pnl == null && startBalance != null && endingBalance != null) {
        pnl = endingBalance - startBalance;
    }
    let roi = firstNumber(cfg.paper_roi_percent);
    if (roi == null && startBalance != null && pnl != null && startBalance !== 0) {
        roi = (pnl / startBalance) * 100;
    }
    const sessionStartedAt = firstValue(cfg.paper_session_started_at);

    card.classList.remove('is-positive', 'is-negative', 'is-flat');
    valueEl.className = 'metric-value mono';

    if (pnl == null) {
        valueEl.textContent = '--';
        subEl.textContent = '等待模拟结果';
        card.classList.add('is-flat');
        return;
    }

    const pnlClass = pnl > 0 ? 'is-positive' : pnl < 0 ? 'is-negative' : 'is-flat';
    card.classList.add(pnlClass);
    valueEl.classList.add(pnl > 0 ? 'c-green' : pnl < 0 ? 'c-red' : 'c-amber');
    valueEl.textContent = formatSignedUSD(pnl);

    const roiText = roi == null ? '--' : `${roi >= 0 ? '+' : ''}${roi.toFixed(2)}%`;
    const startText = startBalance == null ? '--' : formatUSD(startBalance);
    const endText = endingBalance == null ? '--' : formatUSD(endingBalance);
    const sessionText = sessionStartedAt ? `本轮 ${shortMinute(sessionStartedAt)} 起` : '本轮';
    subEl.textContent = `${sessionText} · ${startText} -> ${endText} · ${roiText}`;
}

function renderTradingControl() {
    const btn = document.getElementById('trade-toggle-btn');
    const note = document.getElementById('trade-toggle-note');
    if (!btn) return;

    btn.classList.remove('enabled', 'disabled', 'pending');
    btn.classList.add(dashboardState.tradingEnabled ? 'enabled' : 'disabled');
    if (dashboardState.togglePending) btn.classList.add('pending');
    btn.textContent = dashboardState.tradingEnabled ? '交易已开启' : '交易已关闭';

    if (dashboardState.controlError) {
        btn.title = dashboardState.controlError;
        if (note) note.textContent = dashboardState.controlError;
        return;
    }

    const message = dashboardState.tradingEnabled
        ? '当前允许机器人继续自动开仓；关闭后不再新开仓，已有持仓仍按规则离场。'
        : '当前已关闭自动开仓；已有持仓仍会按止盈和到期规则继续处理。';
    btn.title = message;
    if (note) note.textContent = message;
}

function renderConfig() {
    const cfg = dashboardState.config;
    if (!cfg) return;

    const isReal = getActiveAccountMode() === 'real';
    const mode = (cfg.trading_mode || '--').toUpperCase();
    const paperSummary = dashboardState.paperBalance || {};
    const realSummary = dashboardState.realBalance || {};
    const wallet = isReal
        ? (realSummary.wallet || cfg.wallet)
        : (cfg.wallet || paperSummary.wallet);
    const cashBalance = isReal
        ? firstNumber(realSummary.balance)
        : firstNumber(cfg.cash_balance, paperSummary.cash_balance);
    const reservedBalance = isReal
        ? null
        : firstNumber(cfg.reserved_balance, paperSummary.reserved_balance);
    const openPositions = dashboardState.positionCounts[getActiveAccountMode()];
    const viewLabel = isReal ? '真实账户视图' : '模拟账户视图';

    setText('cfg-mode', cfg.strategy_name ? `${mode} / ${viewLabel}` : `${mode} / ${viewLabel}`);
    setText('cfg-daily-open', cfg.daily_open != null ? formatUSD(cfg.daily_open) : '--');
    setText(
        'cfg-current',
        cfg.signal_price != null
            ? `${formatUSD(cfg.signal_price)} (${Number(cfg.daily_change_percent || 0).toFixed(2)}%)`
            : '--'
    );
    setText('cfg-bet', '$' + (cfg.paper_bet_amount || cfg.bet_amount || '--'));
    setText('cfg-max', cashBalance != null ? formatUSD(cashBalance) : '$' + (cfg.max_bet_amount || '--'));

    if (cfg.max_entry_price !== undefined) {
        const minEntry = cfg.min_entry_price !== undefined ? Number(cfg.min_entry_price).toFixed(2) : '0.00';
        setText('cfg-diff', `${minEntry} - ${Number(cfg.max_entry_price).toFixed(2)}`);
    } else {
        const diff = Number(cfg.min_probability_diff || 0);
        setText('cfg-diff', (diff * 100).toFixed(0) + '%');
    }
    if (cfg.max_spread !== undefined) {
        setText('cfg-spread', '<= ' + Number(cfg.max_spread).toFixed(2));
    }
    if (cfg.min_top_book_size !== undefined) {
        setText('cfg-depth', '>= ' + Number(cfg.min_top_book_size).toFixed(0) + ' shares');
    }

    if (cfg.take_profit_usd !== undefined) {
        setText('cfg-tp', 'best bid 浮盈 > $' + Number(cfg.take_profit_usd).toFixed(2));
    } else {
        setText('cfg-tp', (Number(cfg.take_profit_percent || 0) * 100).toFixed(0) + '%');
    }

    if (cfg.exit_rule) {
        setText('cfg-sl', cfg.exit_rule);
    } else {
        setText('cfg-sl', cfg.stop_loss_enabled === 'true' ? '开启 (' + (Number(cfg.stop_loss_percent) * 100) + '%)' : '关闭');
    }

    setText('cfg-open-positions', `${openPositions || 0} 仓`);
    setText('cfg-reserved', reservedBalance != null ? formatUSD(reservedBalance) : (isReal ? '只读' : '--'));

    const paperProfit = Number(cfg.paper_profit);
    if (!isNaN(paperProfit)) {
        setText('cfg-paper-profit', `${paperProfit >= 0 ? '+' : ''}$${paperProfit.toFixed(2)} (${Number(cfg.paper_roi_percent || 0).toFixed(2)}%)`);
    } else {
        setText('cfg-paper-profit', '--');
    }
    setText('cfg-wallet', wallet || '--');
}

function setAccountMode(mode, shouldRefresh = true) {
    dashboardState.accountMode = mode === 'real' ? 'real' : 'paper';
    dashboardState.controlError = '';
    try {
        window.localStorage.setItem('polymarket_account_mode', dashboardState.accountMode);
    } catch (e) {
        // ignore localStorage issues
    }
    renderAccountMode();
    renderTradingControl();
    renderConfig();
    if (shouldRefresh) {
        Promise.allSettled([fetchTrades(), fetchOrders()]);
    }
}

async function toggleTrading() {
    if (dashboardState.togglePending) return;

    dashboardState.togglePending = true;
    dashboardState.controlError = '';
    renderTradingControl();

    try {
        const resp = await fetch('/api/control', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ trading_enabled: !dashboardState.tradingEnabled }),
        });
        const data = await resp.json();
        if (!resp.ok || data.error) {
            throw new Error(data.error || '控制接口调用失败');
        }

        dashboardState.tradingEnabled = data.trading_enabled !== false;
        await Promise.allSettled([fetchControl(), fetchBotStatus(), fetchConfig()]);
    } catch (e) {
        dashboardState.controlError = '交易开关更新失败: ' + String(e.message || e).substring(0, 40);
    } finally {
        dashboardState.togglePending = false;
        renderTradingControl();
    }
}

/* ---- BTC 价格 ---- */
async function fetchBtc() {
    try {
        const resp = await fetch('/api/btc');
        const data = await resp.json();
        if (data.error) {
            setText('btc-price', '错误');
            setText('btc-change', data.error);
            return;
        }
        setText('btc-price', formatUSD(data.price));
        const ch = Number(data.change_24h);
        const changeEl = document.getElementById('btc-change');
        changeEl.textContent = (ch > 0 ? '+' : '') + ch.toFixed(2) + '% (24h)';
        changeEl.className = 'metric-sub ' + (ch > 0 ? 'c-green' : ch < 0 ? 'c-red' : '');
    } catch (e) {
        setText('btc-price', '离线');
        setText('btc-change', '网络错误');
    }
}

/* ---- 控制状态 ---- */
async function fetchControl() {
    try {
        const resp = await fetch('/api/control?ts=' + Date.now(), { cache: 'no-store' });
        const data = await resp.json();
        dashboardState.tradingEnabled = data.trading_enabled !== false;
        dashboardState.controlError = '';
    } catch (e) {
        dashboardState.controlError = '交易控制状态读取失败';
    }
    renderTradingControl();
    renderConfig();
}

/* ---- Bot 状态 ---- */
async function fetchBotStatus() {
    try {
        const resp = await fetch('/status-json?ts=' + Date.now(), { cache: 'no-store' });
        const data = await resp.json();
        if (!data || Object.keys(data).length === 0) {
            setOffline();
            return;
        }

        if (data.trading_enabled !== undefined) {
            dashboardState.tradingEnabled = data.trading_enabled !== false;
            if (!dashboardState.togglePending) dashboardState.controlError = '';
            renderTradingControl();
        }

        const dot = document.getElementById('status-dot');
        const label = document.getElementById('status-label');
        if (data.running) {
            dot.className = 'status-dot online';
            label.textContent = dashboardState.tradingEnabled ? '机器人运行中 · 交易开启' : '机器人运行中 · 交易关闭';
        } else {
            dot.className = 'status-dot offline';
            label.textContent = 'Bot 已停止';
        }

        const predMap = { UP: 'AI 看涨', DOWN: 'AI 看跌', HOLD: 'AI 观望' };
        const predClass = { UP: 'c-green', DOWN: 'c-red', HOLD: 'c-amber' };
        const pred = (data.ai_prediction || 'HOLD').toUpperCase();
        const predEl = document.getElementById('ai-prediction');
        predEl.textContent = predMap[pred] || pred;
        predEl.className = 'metric-value ' + (predClass[pred] || '');
        if (data.daily_open != null && data.signal_price != null) {
            const relation = Number(data.signal_price) >= Number(data.daily_open) ? '高于' : '低于';
            setText('ai-label', `模型基于日线偏向：现价 ${Number(data.signal_price).toLocaleString()} ${relation} 今开 ${Number(data.daily_open).toLocaleString()}`);
        } else {
            setText('ai-label', pred === 'UP' ? 'AI 判断现价高于今开' : pred === 'DOWN' ? 'AI 判断现价低于今开' : '等待信号');
        }

        if (data.yes_price != null && data.no_price != null) {
            const outcomes = Array.isArray(data.outcomes) ? data.outcomes : ['YES', 'NO'];
            const firstLabel = (outcomes[0] || 'YES').toUpperCase();
            const secondLabel = (outcomes[1] || 'NO').toUpperCase();
            let targetLabel = firstLabel;
            let targetPrice = Number(data.yes_price) * 100;
            let reverseLabel = secondLabel;
            let reversePrice = Number(data.no_price) * 100;

            if (pred === 'DOWN') {
                targetLabel = secondLabel;
                targetPrice = Number(data.no_price) * 100;
                reverseLabel = firstLabel;
                reversePrice = Number(data.yes_price) * 100;
            }

            setOutcomeLabels(targetLabel, reverseLabel);
            setText('yes-price', Math.round(targetPrice) + '¢');
            setText('no-price', Math.round(reversePrice) + '¢');
            setText('prob-yes', targetPrice.toFixed(1) + '% 目标方向');
            setText('prob-no', reversePrice.toFixed(1) + '% 反向盘口');
            setMarketDominance(targetPrice, reversePrice);
        }

        if (data.market) setText('market-name', data.market);
        if (data.last_update) setText('update-time', shortTime(data.last_update));
        renderAiThoughts(data);
        updateDecision(data.decision, data.error, data.decision_reason);
    } catch (e) {
        setOffline();
    }
}

function setOffline() {
    document.getElementById('status-dot').className = 'status-dot offline';
    setText('status-label', '无数据');
}

function renderAiThoughts(data) {
    const card = document.getElementById('ai-thought-card');
    const meta = document.getElementById('ai-thought-meta');
    if (!card || !meta) return;

    const confidence = firstNumber(data.ai_confidence);
    const model = firstValue(data.ai_model, dashboardState.config && dashboardState.config.ai_model, '--');
    const action = firstValue(data.ai_action, data.decision, 'HOLD');
    const source = firstValue(data.ai_source, dashboardState.config && dashboardState.config.ai_source, 'llm');
    const factors = Array.isArray(data.ai_key_factors) ? data.ai_key_factors : [];
    const risks = Array.isArray(data.ai_risk_flags) ? data.ai_risk_flags : [];
    const reasoning = firstValue(data.ai_thought_markdown, data.signal_reason, data.decision_reason, '等待 AI 输出...');
    const intervalSeconds = firstNumber(data.ai_decision_interval_seconds, dashboardState.config && dashboardState.config.ai_decision_interval_seconds);
    const decisionId = firstValue(data.ai_decision_id, dashboardState.config && dashboardState.config.ai_decision_id, '--');

    meta.textContent = `${model} · ${source}${confidence != null ? ` · ${(confidence * 100).toFixed(0)}%` : ''}`;

    const factorHtml = factors.length
        ? factors.map((item) => `<li>${escapeHtml(item)}</li>`).join('')
        : '<li>暂无关键依据</li>';
    const riskHtml = risks.length
        ? risks.map((item) => `<li>${escapeHtml(item)}</li>`).join('')
        : '<li>暂无风险提示</li>';

    card.innerHTML = `
        <div class="thought-summary">${escapeHtml(reasoning)}</div>
        <div class="thought-meta-line mono">决策编号：${escapeHtml(decisionId)} · 动作：${escapeHtml(action)} · 决策频率：${intervalSeconds != null ? intervalSeconds + ' 秒 / 次' : '--'} · 最近同步：${shortTime(data.last_update)}</div>
        <div class="thought-sections">
            <div class="thought-section">
                <div class="thought-section-title">关键依据</div>
                <ul class="thought-list">${factorHtml}</ul>
            </div>
            <div class="thought-section">
                <div class="thought-section-title">风险提示</div>
                <ul class="thought-list">${riskHtml}</ul>
            </div>
        </div>
    `;
}

async function fetchAiHistory() {
    try {
        const resp = await fetch('/api/ai-decisions?ts=' + Date.now(), { cache: 'no-store' });
        const data = await resp.json();
        dashboardState.aiHistory = Array.isArray(data) ? data : [];
        renderAiHistory();
    } catch (e) {
        const list = document.getElementById('ai-history-list');
        if (list) list.innerHTML = '<div class="empty-row">AI 决策历史读取失败</div>';
    }
}

function renderAiHistory() {
    const list = document.getElementById('ai-history-list');
    const count = document.getElementById('ai-history-count');
    if (!list || !count) return;

    const entries = Array.isArray(dashboardState.aiHistory) ? dashboardState.aiHistory : [];
    count.textContent = `${entries.length} 条`;
    if (!entries.length) {
        list.innerHTML = '<div class="empty-row">等待 AI 生成第一条决策记录...</div>';
        return;
    }

    list.innerHTML = entries.slice(0, 10).map((entry) => {
        const decisionId = escapeHtml(firstValue(entry.decision_id, '--'));
        const action = escapeHtml(firstValue(entry.action, entry.decision, 'HOLD'));
        const prediction = escapeHtml(firstValue(entry.prediction, 'HOLD'));
        const model = escapeHtml(firstValue(entry.model, '--'));
        const reasoning = escapeHtml(firstValue(entry.reasoning, entry.thought_markdown, '暂无说明'));
        const confidence = firstNumber(entry.confidence);
        const executionSummary = escapeHtml(firstValue(entry.execution_summary, '等待执行'));
        const linkedTrades = Array.isArray(entry.linked_trades) ? entry.linked_trades : [];
        const candidateMarkets = Array.isArray(entry.candidate_markets) ? entry.candidate_markets : [];

        const candidateHtml = candidateMarkets.length
            ? candidateMarkets.slice(0, 2).map((market) => {
                const upAsk = firstNumber(market.up && market.up.best_ask);
                const downAsk = firstNumber(market.down && market.down.best_ask);
                const mins = firstNumber(market.minutes_to_expiry);
                return `<li>${escapeHtml(firstValue(market.question, '--'))} · UP ask ${upAsk != null ? upAsk.toFixed(3) : '--'} / DOWN ask ${downAsk != null ? downAsk.toFixed(3) : '--'} · 剩余 ${mins != null ? mins.toFixed(1) + ' 分钟' : '--'}</li>`;
            }).join('')
            : '<li>本次没有可用盘口摘要</li>';

        const linkedHtml = linkedTrades.length
            ? linkedTrades.map((trade) => {
                const realized = firstNumber(trade.realized_profit);
                const resultText = realized == null ? escapeHtml(firstValue(trade.status, '进行中')) : `${realized >= 0 ? '+' : ''}$${realized.toFixed(2)}`;
                const resultClass = realized == null ? 'c-amber' : realized >= 0 ? 'c-green' : 'c-red';
                const operation = String(firstValue(trade.side, '')).toUpperCase().includes('SELL') ? '平仓' : '开仓';
                return `<li>
                    <span>${shortTime(firstValue(trade.created_at))} · ${operation} ${escapeHtml(firstValue(trade.outcome, '--'))} · ${escapeHtml(firstValue(trade.market, '--'))}</span>
                    <strong class="${resultClass} mono">${resultText}</strong>
                </li>`;
            }).join('')
            : '<li>这一条 AI 决策目前还没有触发交易。</li>';

        return `<div class="ai-history-card">
            <div class="ai-history-head">
                <div class="ai-history-title-row">
                    <span class="tag tag-ok">${decisionId}</span>
                    <span class="tag ${action === 'BUY' ? 'tag-buy' : action === 'SELL' ? 'tag-sell' : 'tag-ok'}">${action}</span>
                    <span class="tag ${prediction === 'UP' ? 'tag-buy' : prediction === 'DOWN' ? 'tag-sell' : 'tag-ok'}">${prediction}</span>
                </div>
                <div class="ai-history-meta mono">${model}${confidence != null ? ` · ${(confidence * 100).toFixed(0)}%` : ''} · ${shortTime(firstValue(entry.generated_at))}</div>
            </div>
            <div class="ai-history-summary">${reasoning}</div>
            <div class="ai-history-execution">${executionSummary}</div>
            <div class="ai-history-columns">
                <div class="ai-history-section">
                    <div class="ai-history-section-title">盘口依据</div>
                    <ul class="ai-history-list-items">${candidateHtml}</ul>
                </div>
                <div class="ai-history-section">
                    <div class="ai-history-section-title">对应交易</div>
                    <ul class="ai-history-list-items ai-history-trades">${linkedHtml}</ul>
                </div>
            </div>
        </div>`;
    }).join('');
}

function renderDecisionSignal() {
    const card = document.getElementById('openclaw-card');
    const meta = document.getElementById('openclaw-meta');
    if (!card || !meta) return;

    const signal = dashboardState.decisionSignal;
    if (!signal) {
        meta.textContent = '等待信号';
        setText('openclaw-action', '--');
        setText('openclaw-confidence', '--');
        setText('openclaw-source', '--');
        setText('openclaw-reason', '等待 OpenClaw 生成最新建议...');
        card.classList.remove('is-buy', 'is-sell', 'is-hold');
        return;
    }

    const action = String(firstValue(signal.action, 'HOLD')).toUpperCase();
    const confidence = firstNumber(signal.confidence);
    const source = firstValue(signal.source, 'openclaw-cron');
    const ts = firstValue(signal.timestamp, signal.generated_at);
    const reason = firstValue(signal.reason, signal.reasoning, '无说明');

    meta.textContent = `${source} · ${shortTime(ts)}`;
    setText('openclaw-action', action);
    setText('openclaw-confidence', confidence == null ? '--' : `${(confidence * 100).toFixed(0)}%`);
    setText('openclaw-source', source);
    setText('openclaw-reason', reason);

    card.classList.remove('is-buy', 'is-sell', 'is-hold');
    card.classList.add(action === 'BUY' ? 'is-buy' : action === 'SELL' ? 'is-sell' : 'is-hold');
}

async function fetchDecisionSignal() {
    try {
        const resp = await fetch('/api/decision-signal?ts=' + Date.now(), { cache: 'no-store' });
        const data = await resp.json();
        dashboardState.decisionSignal = resp.ok && !data.error ? data : null;
    } catch (e) {
        dashboardState.decisionSignal = null;
    }
    renderDecisionSignal();
}

function updateDecision(decision, error, reason) {
    const tabs = {
        buy: document.getElementById('tab-buy'),
        sell: document.getElementById('tab-sell'),
        hold: document.getElementById('tab-hold'),
    };
    const actionEl = document.getElementById('decision-action');
    const reasonEl = document.getElementById('decision-reason');

    Object.values(tabs).forEach((t) => {
        t.className = 'dec-tab';
    });

    if (error) {
        tabs.hold.className = 'dec-tab active-sell';
        actionEl.textContent = '系统错误';
        actionEl.className = 'decision-action c-red';
        reasonEl.textContent = error;
        return;
    }

    if (decision === 'BUY') {
        tabs.buy.className = 'dec-tab active-buy';
        actionEl.textContent = '买入';
        actionEl.className = 'decision-action c-green';
        reasonEl.textContent = reason || '模型和赔率给出正向共振，适合进场。';
    } else if (decision === 'SELL') {
        tabs.sell.className = 'dec-tab active-sell';
        actionEl.textContent = '卖出';
        actionEl.className = 'decision-action c-red';
        reasonEl.textContent = reason || '风险偏移，优先保护资金。';
    } else {
        tabs.hold.className = 'dec-tab active-hold';
        actionEl.textContent = '观望';
        actionEl.className = 'decision-action c-amber';
        reasonEl.textContent = reason || '暂无足够优势，保持耐心。';
    }
}

/* ---- 余额 ---- */
async function fetchBalance() {
    let fallbackError = '查询失败';
    try {
        const resp = await fetch('/api/balance?ts=' + Date.now(), { cache: 'no-store' });
        const data = await resp.json();
        if (data.error) {
            fallbackError = '余额接口异常: ' + data.error.substring(0, 24);
        } else {
            let balance = null;
            if (typeof data === 'number') balance = data;
            else if (data.balance !== undefined) balance = Number(data.balance);
            else if (data.collateral !== undefined) balance = Number(data.collateral);
            else if (data.available !== undefined) balance = Number(data.available);

            if (balance !== null && !isNaN(balance)) {
                dashboardState.paperBalance = data;
                setText('usdc-balance', formatUSD(balance));
                const source = getBalanceSourceLabel(data.source);
                const wallet = shortWallet(data.wallet);
                if (data.source === 'paper_live') {
                    const realized = Number(data.realized_pnl || 0);
                    const unrealized = Number(data.unrealized_pnl || 0);
                    const cash = Number(data.cash_balance || 0);
                    const reserved = Number(data.reserved_balance || 0);
                    setText('balance-status', `${wallet} · 现金 ${cash.toFixed(2)} / 占用 ${reserved.toFixed(2)} · 已实现 ${formatSignedUSD(realized)} / 未实现 ${formatSignedUSD(unrealized)}`);
                } else {
                    setText('balance-status', '已连接 ' + wallet + ' · ' + source);
                }
                renderPaperPerformance();
                renderConfig();
                return;
            }
            fallbackError = JSON.stringify(data).substring(0, 40);
        }
    } catch (e) {
        fallbackError = '查询失败';
    }

    try {
        const resp = await fetch('/api/config?ts=' + Date.now(), { cache: 'no-store' });
        const cfg = await resp.json();
        if (cfg.paper_balance !== undefined && !isNaN(Number(cfg.paper_balance))) {
            dashboardState.paperBalance = {
                balance: Number(cfg.paper_balance),
                wallet: cfg.wallet,
                cash_balance: cfg.cash_balance,
                reserved_balance: cfg.reserved_balance,
            };
            setText('usdc-balance', formatUSD(cfg.paper_balance));
            const cash = cfg.cash_balance != null ? formatUSD(cfg.cash_balance) : '--';
            const reserved = cfg.reserved_balance != null ? formatUSD(cfg.reserved_balance) : '--';
            setText('balance-status', `LOCAL-SIM-100U · 配置回退 · 现金 ${cash} / 占用 ${reserved}`);
            renderPaperPerformance();
            renderConfig();
            return;
        }
    } catch (e) {
        // ignore fallback errors
    }

    setText('usdc-balance', '--');
    setText('balance-status', fallbackError);
    renderPaperPerformance();
}

async function fetchRealBalance() {
    try {
        const resp = await fetch('/api/real-balance?ts=' + Date.now(), { cache: 'no-store' });
        const data = await resp.json();
        if (data.error) {
            setText('real-usdc-balance', '--');
            setText('real-balance-status', '真实钱包查询失败: ' + data.error.substring(0, 24));
            return;
        }

        const balance = data.balance !== undefined ? Number(data.balance) : NaN;
        if (isNaN(balance)) {
            setText('real-usdc-balance', '--');
            setText('real-balance-status', '真实钱包余额格式异常');
            return;
        }

        dashboardState.realBalance = data;
        setText('real-usdc-balance', formatUSD(balance));
        const wallet = shortWallet(data.wallet);
        const source = getBalanceSourceLabel(data.source);
        setText('real-balance-status', `${wallet} · 可用现金 · ${source}`);
        renderConfig();
    } catch (e) {
        setText('real-usdc-balance', '--');
        setText('real-balance-status', '真实钱包查询失败');
    }
}

/* ---- 最近交易 ---- */
async function fetchTrades() {
    try {
        const mode = getActiveAccountMode();
        const resp = await fetch(`/api/trades?account=${mode}&ts=` + Date.now(), { cache: 'no-store' });
        const data = await resp.json();
        const tbody = document.getElementById('trades-body');

        if (data.error || !Array.isArray(data)) {
            const items = data.data || data.trades || data;
            if (!Array.isArray(items)) {
                tbody.innerHTML = `<tr><td colspan="${getTradeColspan()}" class="empty-row">${escapeHtml(data.error || getEmptyTradeMessage())}</td></tr>`;
                setText('trade-count', '0 笔');
                return;
            }
            renderTrades(items);
            return;
        }
        renderTrades(data);
    } catch (e) {
        document.getElementById('trades-body').innerHTML = `<tr><td colspan="${getTradeColspan()}" class="empty-row">${escapeHtml(getEmptyTradeMessage())}</td></tr>`;
    }
}

function renderTrades(trades) {
    const tbody = document.getElementById('trades-body');
    setText('trade-count', trades.length + ' 笔');

    if (!trades.length) {
        tbody.innerHTML = `<tr><td colspan="${getTradeColspan()}" class="empty-row">${escapeHtml(getEmptyTradeMessage())}</td></tr>`;
        return;
    }

    const rows = trades.map((t) => {
        const side = String(firstValue(t.side, t.type, '') || '').toUpperCase();
        const outcome = String(firstValue(t.outcome, t.outcome_name, t.label, '') || '').toUpperCase();
        const decisionId = firstValue(t.ai_decision_id, t.decision_id, '');
        const sideText = side.includes('BUY')
            ? ('买入 ' + (outcome || ''))
            : side.includes('SELL')
                ? ('卖出 ' + (outcome || ''))
                : (outcome || side || '--');
        const sideTag = `<span class="tag ${side.includes('BUY') ? 'tag-buy' : side.includes('SELL') ? 'tag-sell' : 'tag-ok'}">${sideText.trim()}</span>`;

        const rawStatus = String(firstValue(t.status, t.tradeStatus, t.state, '') || '').toUpperCase();
        const isOpenAction = rawStatus.includes('OPEN');
        const operationTag = `<span class="tag ${isOpenAction ? 'tag-buy' : 'tag-sell'}">${isOpenAction ? '开仓' : '平仓'}</span>`;

        const time = shortTime(firstValue(t.created_at, t.timestamp, t.match_time, t.time));
        const amountRaw = firstValue(t.amount_display, t.size_display, t.size, t.amount, t.quantity, t.lastSize);
        const amount = amountRaw == null ? '--' : String(amountRaw);
        const price = firstNumber(t.price, t.avgPrice, t.avg_price, t.executionPrice);
        const market = firstValue(t.market, t.question, t.title, t.name, '--');
        const note = firstValue(t.note, t.description, t.reason, '');
        const realizedPnl = firstNumber(t.realized_profit, t.realizedPnl, t.pnl, t.profit, extractPnlFromText(note));

        let resultTag = '<span class="tag tag-ok">进行中</span>';
        let resultValue = '<span class="trade-result-value mono">--</span>';
        if (!isOpenAction && realizedPnl != null) {
            if (realizedPnl > 0) resultTag = '<span class="tag tag-buy">盈利</span>';
            else if (realizedPnl < 0) resultTag = '<span class="tag tag-sell">亏损</span>';
            else resultTag = '<span class="tag tag-ok">保本</span>';
            resultValue = `<span class="trade-result-value mono ${realizedPnl > 0 ? 'c-green' : realizedPnl < 0 ? 'c-red' : 'c-amber'}">${formatSignedUSD(realizedPnl)}</span>`;
        } else if (!isOpenAction) {
            if (rawStatus.includes('TAKE_PROFIT')) {
                resultTag = '<span class="tag tag-buy">止盈</span>';
            } else if (rawStatus.includes('STOP_LOSS')) {
                resultTag = '<span class="tag tag-sell">止损</span>';
            } else if (rawStatus.includes('TIME_EXIT') || rawStatus.includes('RESOLUTION')) {
                resultTag = '<span class="tag tag-ok">离场</span>';
            } else {
                resultTag = '<span class="tag tag-ok">已平仓</span>';
            }
        }

        const noteId = `trade-note-${escapeHtml(String(firstValue(t.id, time, Math.random())).replace(/[^a-zA-Z0-9_-]/g, '-'))}`;
        const detailParts = [];
        if (decisionId) {
            detailParts.push(`<div class="trade-decision-link"><span class="tag tag-ok">${escapeHtml(decisionId)}</span><span>对应的 AI 决策记录</span></div>`);
        }
        detailParts.push(`<div class="trade-market">${escapeHtml(market)}</div>`);
        if (note) {
            detailParts.push(`
                <details class="trade-note-wrap">
                    <summary class="trade-note-summary">查看说明</summary>
                    <div class="trade-note" id="${noteId}">${escapeHtml(note)}</div>
                </details>
            `);
        }

        return `<tr>
            <td>${time}</td>
            <td>${operationTag}</td>
            <td>${sideTag}</td>
            <td>${escapeHtml(amount)}</td>
            <td>${price != null ? price.toFixed(4) : '--'}</td>
            <td><div class="trade-result">${resultTag}${resultValue}</div></td>
            <td><div class="trade-detail trade-detail-compact">${detailParts.join('')}</div></td>
        </tr>`;
    }).join('');

    tbody.innerHTML = rows;
}

/* ---- Order Book ---- */
async function fetchOrderBook() {
    try {
        const resp = await fetch('/api/orderbook?ts=' + Date.now(), { cache: 'no-store' });
        const data = await resp.json();
        const container = document.getElementById('orderbook-grid');

        if (data.error) {
            container.innerHTML = '<div class="empty-row">' + data.error.substring(0, 40) + '</div>';
            return;
        }

        const outcomes = Array.isArray(data.outcomes) ? data.outcomes : [];
        if (!outcomes.length) {
            container.innerHTML = '<div class="empty-row">No book available</div>';
            return;
        }

        container.innerHTML = outcomes.slice(0, 2).map((book, index) => {
            const bids = Array.isArray(book.bids) ? book.bids.slice(0, 3) : [];
            const asks = Array.isArray(book.asks) ? book.asks.slice(0, 3) : [];
            const rows = [0, 1, 2].map((rowIndex) => {
                const bid = bids[rowIndex];
                const ask = asks[rowIndex];
                return `<div class="orderbook-row">
                    <span class="orderbook-price orderbook-bid mono">${bid ? Number(bid.price).toFixed(3) : '--'}</span>
                    <span class="orderbook-size mono">${bid ? bid.size : '--'}</span>
                    <span class="orderbook-divider">|</span>
                    <span class="orderbook-price orderbook-ask mono">${ask ? Number(ask.price).toFixed(3) : '--'}</span>
                    <span class="orderbook-size mono">${ask ? ask.size : '--'}</span>
                </div>`;
            }).join('');

            return `<div class="orderbook-card ${index === 0 ? 'orderbook-up' : 'orderbook-down'}">
                <div class="orderbook-head">
                    <span class="tag ${index === 0 ? 'tag-buy' : 'tag-sell'}">${(book.label || '--').toUpperCase()}</span>
                    <div class="orderbook-meta">
                        <span class="orderbook-mid mono">${book.mid != null ? Math.round(Number(book.mid) * 100) + '¢' : '--'}</span>
                        <span class="orderbook-spread mono">${book.spread != null ? `点差 ${Math.round(Number(book.spread) * 100)}¢` : '点差 --'}</span>
                    </div>
                </div>
                <div class="orderbook-columns">
                    <span>Bids</span>
                    <span>Asks</span>
                </div>
                ${rows}
            </div>`;
        }).join('');
    } catch (e) {
        document.getElementById('orderbook-grid').innerHTML = '<div class="empty-row">Book fetch failed</div>';
    }
}

/* ---- 当前持仓 ---- */
async function fetchOrders() {
    try {
        const mode = getActiveAccountMode();
        const resp = await fetch(`/api/positions?account=${mode}&ts=` + Date.now(), { cache: 'no-store' });
        const data = await resp.json();
        const container = document.getElementById('order-list');

        if (data.error) {
            container.innerHTML = '<div class="empty-row">' + data.error.substring(0, 40) + '</div>';
            return;
        }

        const positions = Array.isArray(data) ? data : (data.positions || data.data || []);
        dashboardState.positionCounts[mode] = positions.length;
        setText('position-count', `${positions.length} 仓`);
        renderConfig();

        if (!positions.length) {
            container.innerHTML = `<div class="empty-row">${getEmptyPositionMessage()}</div>`;
            return;
        }

        container.innerHTML = positions.slice(0, 6).map((p) => {
            const positionId = firstValue(p.id, p.position_id, p.market_slug, p.market, p.question, '--');
            const outcome = String(firstValue(p.outcome, p.outcome_name, p.label, '') || '').toUpperCase();
            const entryPrice = firstNumber(p.entry_price, p.avgPrice, p.avg_price, p.buy_price, p.price);
            const markPrice = firstNumber(p.mark_price, p.current_price, p.currentPrice, p.current_price_value, p.price);
            const bidPrice = firstNumber(p.bid_price, p.best_bid, p.exit_bid, p.sell_price, markPrice);
            const askPrice = firstNumber(p.ask_price, p.best_ask, p.entry_ask, entryPrice);
            const spread = firstNumber(p.spread);
            const shares = firstNumber(p.shares, p.size, p.quantity, p.position_size);
            const stake = firstNumber(p.stake, p.initialValue, p.initial_value, p.amount, p.cost_basis, p.costBasis);
            let currentValue = firstNumber(p.current_value, p.currentValue, p.value, p.market_value);
            if (currentValue == null && markPrice != null && shares != null) {
                currentValue = markPrice * shares;
            }
            let liquidationValue = firstNumber(p.liquidation_value);
            if (liquidationValue == null && bidPrice != null && shares != null) {
                liquidationValue = bidPrice * shares;
            }
            let pnl = firstNumber(p.unrealized_profit, p.unrealizedPnl, p.unrealized_pnl, p.pnl);
            if (pnl == null && liquidationValue != null && stake != null) {
                pnl = liquidationValue - stake;
            }

            const endTime = shortTime(firstValue(p.end_date, p.endDate, p.expiration, p.expiry));
            const label = firstValue(p.market, p.question, p.title, p.name, '--');
            const pnlClass = pnl != null && pnl > 0 ? 'is-profit' : pnl != null && pnl < 0 ? 'is-loss' : 'is-flat';
            const spreadText = spread != null ? `${(spread * 100).toFixed(1)}¢` : '--';
            const liquidationText = formatUSD(liquidationValue != null ? liquidationValue : currentValue);
            const expandedClass = dashboardState.expandedPositionId === positionId ? ' is-expanded' : '';
            const collapsedSummary = [
                `本金 ${formatUSD(stake)}`,
                `可卖 ${liquidationText}`,
                `到期 ${endTime}`,
            ].join(' · ');

            return `<div class="order-item position-card ${pnlClass}${expandedClass}" data-position-id="${positionId}">
                <button class="position-toggle" type="button" aria-expanded="${expandedClass ? 'true' : 'false'}" onclick="togglePositionCard(this)">
                    <div class="position-card-top">
                        <div class="position-card-main">
                            <span class="tag ${pnl != null && pnl >= 0 ? 'tag-buy' : 'tag-sell'}">${outcome || '持仓'}</span>
                            <span class="position-market">${label}</span>
                        </div>
                        <div class="position-pnl-block">
                            <span class="position-pnl-label">浮盈</span>
                            <strong class="position-pnl-value mono">${formatSignedUSD(pnl)}</strong>
                        </div>
                    </div>
                    <div class="position-collapsed-row">
                        <span class="position-collapsed-summary mono">${collapsedSummary}</span>
                        <span class="position-expand-indicator">
                            <span class="position-expand-label">展开详情</span>
                            <span class="position-expand-chevron">⌄</span>
                        </span>
                    </div>
                </button>
                <div class="position-card-details">
                    <div class="position-value-strip mono">
                        <span class="position-value-item"><span>本金</span><strong>${formatUSD(stake)}</strong></span>
                        <span class="position-value-arrow">→</span>
                        <span class="position-value-item"><span>可卖</span><strong>${liquidationText}</strong></span>
                    </div>
                    <div class="position-stat-grid">
                        <div class="position-stat"><span>入场 ask</span><strong class="mono">${askPrice != null ? askPrice.toFixed(4) : (entryPrice != null ? entryPrice.toFixed(4) : '--')}</strong></div>
                        <div class="position-stat"><span>当前 bid</span><strong class="mono">${bidPrice != null ? bidPrice.toFixed(4) : '--'}</strong></div>
                        <div class="position-stat"><span>中间价</span><strong class="mono">${markPrice != null ? markPrice.toFixed(4) : '--'}</strong></div>
                        <div class="position-stat"><span>点差</span><strong class="mono">${spreadText}</strong></div>
                        <div class="position-stat"><span>份额</span><strong class="mono">${shares != null ? shares.toFixed(4) : '--'}</strong></div>
                        <div class="position-stat"><span>到期</span><strong class="mono">${endTime}</strong></div>
                    </div>
                </div>
            </div>`;
        }).join('');
    } catch (e) {
        document.getElementById('order-list').innerHTML = `<div class="empty-row">${getEmptyPositionMessage()}</div>`;
    }
}

/* ---- 配置 ---- */
async function fetchConfig() {
    try {
        const resp = await fetch('/api/config?ts=' + Date.now(), { cache: 'no-store' });
        const cfg = await resp.json();
        dashboardState.config = cfg;
        if (cfg.trading_enabled !== undefined && !dashboardState.togglePending) {
            dashboardState.tradingEnabled = cfg.trading_enabled !== false;
            dashboardState.controlError = '';
            renderTradingControl();
        }
        renderPaperPerformance();
        renderConfig();
    } catch (e) {
        // ignore config fetch failures
    }
}

function togglePositionCard(button) {
    const card = button && button.closest('.position-card');
    if (!card) return;
    const container = card.parentElement;
    const willExpand = !card.classList.contains('is-expanded');
    const positionId = card.getAttribute('data-position-id');

    if (container) {
        container.querySelectorAll('.position-card.is-expanded').forEach((item) => {
            if (item === card) return;
            item.classList.remove('is-expanded');
            const toggle = item.querySelector('.position-toggle');
            const label = item.querySelector('.position-expand-label');
            if (toggle) toggle.setAttribute('aria-expanded', 'false');
            if (label) label.textContent = '展开详情';
        });
    }

    card.classList.toggle('is-expanded', willExpand);
    button.setAttribute('aria-expanded', willExpand ? 'true' : 'false');
    const label = card.querySelector('.position-expand-label');
    if (label) label.textContent = willExpand ? '收起详情' : '展开详情';
    dashboardState.expandedPositionId = willExpand ? positionId : null;
}

/* ---- 全局刷新 ---- */
async function refreshAll() {
    const btn = document.getElementById('refresh-btn');
    btn.classList.add('spinning');
    setTimeout(() => btn.classList.remove('spinning'), 600);

    await Promise.allSettled([
        fetchBtc(),
        fetchControl(),
        fetchBotStatus(),
        fetchBalance(),
        fetchRealBalance(),
        fetchTrades(),
        fetchAiHistory(),
        fetchDecisionSignal(),
        fetchOrderBook(),
        fetchOrders(),
        fetchConfig(),
    ]);

    setText('update-time', new Date().toLocaleTimeString('zh-CN'));
}

window.setAccountMode = setAccountMode;
window.toggleTrading = toggleTrading;
window.togglePositionCard = togglePositionCard;
window.refreshAll = refreshAll;

renderAccountMode();
renderTradingControl();
renderDecisionSignal();
fetchConfig();
refreshAll();
setInterval(refreshAll, 10000);

// ========== Simmer ==========
const SIMMER_API = 'https://api.simmer.markets/api/sdk';
let simmerCurrentTab = 'polymarket';
let simmerRefreshTimer = null;

function switchPlatform(platform) {
    simmerCurrentTab = platform;
    document.getElementById('panel-polymarket').style.display = platform === 'polymarket' ? '' : 'none';
    document.getElementById('simmer-panel').style.display = platform === 'simmer' ? '' : 'none';
    document.getElementById('tab-polymarket').classList.toggle('active', platform === 'polymarket');
    document.getElementById('tab-simmer').classList.toggle('active', platform === 'simmer');
    document.getElementById('brand-line-bot').style.display = platform === 'polymarket' ? '' : 'none';
    document.getElementById('brand-line-simmer').style.display = platform === 'simmer' ? '' : 'none';
    if (platform === 'simmer') {
        loadSimmerData();
        if (!simmerRefreshTimer) simmerRefreshTimer = setInterval(loadSimmerData, 60000);
    } else {
        if (simmerRefreshTimer) { clearInterval(simmerRefreshTimer); simmerRefreshTimer = null; }
    }
}

async function simmerApi(path) {
    const key = 'sk_live_YOUR_STRIPE_KEY_HERE';
    const res = await fetch(SIMMER_API + path, {
        headers: { 'Authorization': 'Bearer ' + key }
    });
    if (!res.ok) throw new Error('API error: ' + res.status);
    return res.json();
}

async function loadSimmerData() {
    try {
        const [me, opp, positions, trades] = await Promise.all([
            simmerApi('/agents/me').catch(() => null),
            simmerApi('/markets/opportunities').catch(() => null),
            simmerApi('/positions').catch(() => null),
            simmerApi('/trades?limit=50').catch(() => null),
        ]);
        if (me) renderSimmerAgent(me);
        if (opp) renderSimmerOpportunities(opp);
        if (positions) renderSimmerPositions(positions);
        if (trades) renderSimmerHistory(trades);
    } catch(e) { console.error('Simmer load error:', e); }
}

function renderSimmerAgent(me) {
    // 如果 Simmer 的 me 数据有交易记录，用 Simmer；否则用本地 Bot 数据
    if (me && me.trades_count > 0) {
        setText('sim-balance', (me.balance || 0).toFixed(2));
        setText('sim-agent-status', me.status === 'claimed' ? '已认领' : me.status);
        setText('sim-agent-sub', me.wallet_address ? shortWallet(me.wallet_address) : 'unclaimed');
        setText('sim-pnl', formatSignedUSD(me.total_pnl || 0));
        const pnlEl = document.getElementById('sim-pnl');
        pnlEl.className = 'metric-value mono ' + ((me.total_pnl || 0) >= 0 ? 'is-positive' : 'is-negative');
        setText('sim-trades-count', me.trades_count || 0);
        setText('sim-win-rate', me.win_rate != null ? '胜率 ' + (me.win_rate * 100).toFixed(1) + '%' : '--');
    } else {
        // 使用本地 Bot 的真实统计数据
        fetch('/api/bot-stats', {cache: 'no-store'})
            .then(r => r.ok ? r.json() : null)
            .then(stats => {
                if (stats) {
                    setText('sim-trades-count', stats.total_trades || 0);
                    setText('sim-win-rate', stats.win_rate != null ? '胜率 ' + stats.win_rate.toFixed(1) + '%' : '--');
                }
            })
            .catch(() => {});
        // Bot 余额
        fetch('/api/balance', {cache: 'no-store'})
            .then(r => r.ok ? r.json() : null)
            .then(bal => {
                if (bal) {
                    setText('sim-balance', (bal.cash_balance || 0).toFixed(2));
                    const realized = bal.realized_pnl || 0;
                    setText('sim-pnl', formatSignedUSD(realized));
                    const pnlEl = document.getElementById('sim-pnl');
                    if (pnlEl) pnlEl.className = 'metric-value mono ' + (realized >= 0 ? 'is-positive' : 'is-negative');
                }
            })
            .catch(() => {});
        setText('sim-agent-status', '本地Bot');
        setText('sim-agent-sub', '已同步');
    }
}

function renderSimmerOpportunities(data) {
    const tbody = document.getElementById('sim-opportunities-body');
    const opps = (data.opportunities || []).filter(o => !isExpired(o.resolves_at)).slice(0, 15);
    setText('sim-opp-count', opps.length + ' 个');
    if (!opps.length) {
        tbody.innerHTML = '<tr><td colspan="5" class="empty-row">暂无可交易机会</td></tr>';
        return;
    }
    tbody.innerHTML = opps.map(o => {
        const prob = ((o.current_probability || 0) * 100).toFixed(1);
        const div = ((o.divergence || 0) * 100).toFixed(1);
        const side = o.recommended_side === 'yes' ? 'YES' : 'NO';
        const sideClass = o.recommended_side === 'yes' ? 'tag-buy' : 'tag-sell';
        const exp = o.resolves_at ? shortTime(o.resolves_at) : '--';
        return `<tr onclick="fillSimmerMarket('${o.id}')" style="cursor:pointer">
            <td><span class="market-question" title="${escapeHtml(o.question)}">${escapeHtml(truncate(o.question, 40))}</span></td>
            <td class="mono">${prob}%</td>
            <td><span class="tag ${sideClass}">${side}</span></td>
            <td class="mono" style="color:${div>0?'#10b981':'#f87171'}">${div > 0 ? '+' : ''}${div}%</td>
            <td class="mono">${exp}</td>
        </tr>`;
    }).join('');
}

function renderSimmerPositions(data) {
    const tbody = document.getElementById('sim-positions-body');
    const positions = data.positions || [];
    setText('sim-pos-count', positions.length + ' 仓');
    if (!positions.length) {
        tbody.innerHTML = '<tr><td colspan="4" class="empty-row">无持仓</td></tr>';
        return;
    }
    tbody.innerHTML = positions.map(p => {
        const prob = ((p.current_probability || 0) * 100).toFixed(1);
        return `<tr>
            <td><span class="market-question">${escapeHtml(truncate(p.question || p.market_question || '—'), 35)}</span></td>
            <td><span class="tag ${p.side === 'yes' ? 'tag-buy' : 'tag-sell'}">${p.side?.toUpperCase()}</span></td>
            <td class="mono">${p.shares || 0}</td>
            <td class="mono">${formatUSD(p.value || 0)}</td>
        </tr>`;
    }).join('');
}

function renderSimmerHistory(data) {
    const tbody = document.getElementById('sim-history-body');
    const trades = data.trades || [];
    setText('sim-hist-count', trades.length + ' 笔');
    if (!trades.length) {
        tbody.innerHTML = '<tr><td colspan="5" class="empty-row">暂无交易</td></tr>';
        return;
    }
    tbody.innerHTML = trades.slice(0, 30).map(t => {
        const pnl = t.realized_pnl || t.pnl || 0;
        const pnlStr = pnl >= 0 ? '<span style="color:#10b981">+' + pnl.toFixed(2) + '</span>' : '<span style="color:#f87171">' + pnl.toFixed(2) + '</span>';
        return `<tr>
            <td class="mono">${t.created_at ? shortTime(t.created_at) : '--'}</td>
            <td><span class="market-question">${escapeHtml(truncate(t.question || t.market_question || '—', 25))}</span></td>
            <td><span class="tag ${t.side === 'yes' ? 'tag-buy' : 'tag-sell'}">${t.side?.toUpperCase()}</span></td>
            <td class="mono">${formatUSD(t.amount || 0)}</td>
            <td>${pnlStr}</td>
        </tr>`;
    }).join('');
}

function fillSimmerMarket(id) {
    document.getElementById('sim-market-id').value = id;
}

async function simmerTrade() {
    const marketId = document.getElementById('sim-market-id').value.trim();
    const side = document.getElementById('sim-side').value;
    const amount = parseFloat(document.getElementById('sim-amount').value) || 10;
    const reasoning = document.getElementById('sim-reasoning').value.trim();
    const source = document.getElementById('sim-source').value;
    const resultEl = document.getElementById('sim-trade-result');

    if (!marketId) { resultEl.innerHTML = '<span style="color:#f87171">请填写 Market ID</span>'; return; }
    if (!reasoning) { resultEl.innerHTML = '<span style="color:#f87171">请填写交易理由</span>'; return; }

    resultEl.textContent = '🔮 执行中...';
    try {
        const key = 'sk_live_YOUR_STRIPE_KEY_HERE';
        const res = await fetch(SIMMER_API + '/trade', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json' },
            body: JSON.stringify({ market_id: marketId, side, amount, reasoning, source })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || data.message || 'Trade failed');
        resultEl.innerHTML = `<span style="color:#10b981">✅ 成功！买入 ${data.shares_bought || '?'} shares</span>`;
        setTimeout(loadSimmerData, 2000);
    } catch(e) {
        resultEl.innerHTML = `<span style="color:#f87171">❌ ${e.message}</span>`;
    }
}

function truncate(str, len) {
    if (!str) return '—';
    return str.length > len ? str.slice(0, len) + '…' : str;
}

function isExpired(iso) {
    if (!iso) return false;
    return new Date(iso) < new Date();
}
