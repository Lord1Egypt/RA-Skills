/**
 * 电机设计参数计算器 v2
 * 支持：极槽配合、匝数设计、磁密验算、反电动势、转矩常数、选型推荐
 *
 * 用法:
 *   node calculator.js poles=8 slots=36 freq=50 speed=3000 boreD=54 coreL=60 airGap=0.5 Br=1.25 Ns=28 a=2
 *   node calculator.js --interactive
 *   node calculator.js --mode compare_slots
 */

const assert = require('assert');

// ============================================================
// 核心计算函数
// ============================================================

function deg2rad(d) { return d * Math.PI / 180; }
function rad2deg(r) { return r * 180 / Math.PI; }

/**
 * 极槽配合计算
 */
function calculatePoleSlot(poles, slots, phases = 3) {
    const p = poles / 2;
    const q = slots / (poles * phases);  // 每极每相槽数
    const slotPerPole = slots / poles;
    const isFractional = !Number.isInteger(q);

    // 每槽机械角度
    const mechAnglePerSlot = 360 / slots;  // deg
    const elecAnglePerSlot = mechAnglePerSlot * p;  // deg

    // 绕组分布系数（60°相带）
    const alpha = deg2rad(elecAnglePerSlot);  // 每槽电气角度
    let kd = 1.0;
    if (q > 1) {
        kd = Math.sin(q * alpha / 2) / (q * Math.sin(alpha / 2));
    }

    // 短距系数（默认 5/6 节距 y=5τ/6）
    const y = Math.round(slotPerPole * 5 / 6);  // 槽数
    const shortPitchRatio = y / slotPerPole;
    const kp = shortPitchRatio < 1 ? shortPitchRatio : 1.0;
    const kw = kd * kp;

    // 槽配合类型判断
    let slotType = '整数槽绕组';
    if (isFractional) {
        if (q < 1) slotType = '分数槽集中绕组';
        else slotType = '分数槽绕组';
    }

    return {
        p, q, slotPerPole, isFractional, slotType,
        mechAnglePerSlot, elecAnglePerSlot,
        kd, kp, kw, y, shortPitchRatio,
        slots, poles, phases
    };
}

/**
 * 气隙磁密与磁通计算
 */
function calculateFluxDensity(poles, slots, boreDiameter, coreLength, airGap, Br, hm, sigma = 1.2) {
    const p = poles / 2;
    const tau = Math.PI * boreDiameter / poles;  // 极距 mm

    // 极弧宽度估算（假设极弧系数 0.8）
    const poleArcWidth = tau * 0.8;
    const Am = poleArcWidth * coreLength;  // 永磁体投影面积 mm²
    const Ae = tau * coreLength;           // 气隙截面积 mm²

    // 气隙磁密估算
    const Bg = sigma * Br * Am / (airGap * Ae);
    const Phi_g = Bg * Ae * 1e-6;  // Wb

    // 齿部磁密估算（简化）
    const toothWidth = tau / 3;  // 齿宽约为极距的1/3
    const slotPitch = Math.PI * boreDiameter / slots;
    const slotWidth = slotPitch - toothWidth;
    const At = toothWidth * coreLength;  // 齿部截面积 mm²
    const B_t = Phi_g * 2 / (At * 1e-6);  // 齿部磁密 T（双侧通量）

    // 轭部磁密估算
    const yokeHeight = tau / 3;
    const Ay = yokeHeight * coreLength;
    const B_y = Phi_g / (Ay * 1e-6) / 2;  // 轭部磁密 T

    return { tau, Bg, Phi_g, B_t, B_y, Am, Ae };
}

/**
 * 每相串联匝数和反电动势计算
 */
function calculateEMF(params) {
    const {
        poles, slots, phases, freq, speed,
        boreDiameter, coreLength, airGap, Br, hm, Ns = 28, a = 2,
        sigma = 1.2, kw = 0.933
    } = params;

    const p = poles / 2;

    // 每相串联匝数
    const Nph = slots * Ns / (2 * a);

    // 气隙磁通
    const fd = calculateFluxDensity(poles, slots, boreDiameter, coreLength, airGap, Br, hm, sigma);
    const Phi_g = fd.Phi_g;

    // 反电动势（线间有效值）
    // E = 4.44 * f * Nph * Kw * Phi_g * 2 (线间)
    const Ke_line_rms = 4.44 * freq * Nph * kw * Phi_g * 2;  // V @ freq Hz
    // 机械转速对应
    const n_sync = 120 * freq / poles;  // 同步转速 rpm
    const Ke_at_speed = Ke_line_rms * speed / n_sync;  // V @ 实际转速

    // 转矩常数
    const omega_e = 2 * Math.PI * freq;  // rad/s 电气角速度
    const Psi_m = Phi_g * kw * Nph;     // 简化磁链
    const Kt = 1.5 * p * Psi_m;         // Nm/A

    return {
        Nph, Kw: kw, Phi_g,
        Ke_line_rms, Ke_at_speed,
        Kt, n_sync,
        freq, speed
    };
}

/**
 * 齿槽转矩估算
 */
function estimateCoggingTorque(poles, slots, Br, R_ro, L) {
    // 齿槽转矩与 (Br^2 * slot_num * pole_num) 相关
    // 简化经验公式：T_cog ∝ (Br^2 * Q * p * R^2 * L) / (g^2)
    // 此处给出一个相对估算值
    const p = poles / 2;
    const airGap = 0.5;  // 默认气隙
    const T_cog_ratio = Br * Br * slots * p * Math.pow(R_ro/50, 2) * (L/50) / Math.pow(airGap, 2);
    const T_cog_estimate = T_cog_ratio * 0.0001;  // Nm，经验系数

    // 判断大小
    let level = '正常';
    if (T_cog_ratio > 500) level = '⚠️ 偏大，建议斜槽/斜极';
    if (T_cog_ratio > 1000) level = '❌ 过大，必须优化';

    return { T_cog_estimate, T_cog_ratio, level };
}

/**
 * 绕组电流和功率估算
 */
function calculatePower(params) {
    const {
        slots, phases, Ns = 28, a = 2,
        Vdc = 48, Idc = 10,
        boreDiameter, coreLength, airGap,
        poles, Br, hm, freq, kw
    } = params;

    const Nph = slots * Ns / (2 * a);
    const Jc = Idc / (Ns * Math.PI * 0.4 * 0.4);  // 估算电流密度 A/mm²
    const I_phase_rms = Idc / Math.sqrt(2);  // 方波驱动有效值

    const fd = calculateFluxDensity(poles, slots, boreDiameter, coreLength, airGap, Br, hm);
    const n_sync = 120 * freq / poles;
    const Ke = 4.44 * freq * Nph * kw * fd.Phi_g * 2;
    const E_line_rms = Ke * Idc / n_sync;  // 近似

    const P_mech = 3 * I_phase_rms * E_line_rms / 2 * 0.85;  // W（效率约0.85）
    const T_out = P_mech / (n_sync * 2 * Math.PI / 60);  // Nm

    return {
        Jc, I_phase_rms,
        P_mech, T_out,
        E_line_rms, Vdc,
        efficiency: 0.85
    };
}

/**
 * 完整极槽配合报告
 */
function generateReport(params) {
    const {
        poles = 8, slots = 36, phases = 3,
        freq = 50, speed = 3000,
        boreDiameter = 54, coreLength = 60,
        airGap = 0.5, Br = 1.25, Hc = 955,
        Ns = 28, a = 2
    } = params;

    const ps = calculatePoleSlot(poles, slots, phases);
    const fd = calculateFluxDensity(poles, slots, boreDiameter, coreLength, airGap, Br, 3, 1.2);
    const emf = calculateEMF({...params, kw: ps.kw});
    const cogging = estimateCoggingTorque(poles, slots, Br, boreDiameter / 2000, coreLength / 1000);
    const power = calculatePower({...params, kw: ps.kw});

    // 磁密合理性检查
    let magCheck = '✅ 磁密分布合理';
    if (fd.Bg > 1.1) magCheck = '⚠️ 气隙磁密偏高(Bg>' + fd.Bg.toFixed(3) + 'T)，铁心可能饱和';
    if (fd.B_t > 1.8) magCheck = '⚠️ 齿部磁密偏高(Bt>' + fd.B_t.toFixed(3) + 'T)';
    if (fd.B_y > 1.6) magCheck = '⚠️ 轭部磁密偏高(By>' + fd.B_y.toFixed(3) + 'T)';

    // 反电动势合理性
    let emfCheck = '✅ 反电动势合理';
    if (emf.Ke_at_speed > Vdc * 0.9) emfCheck = '⚠️ 反电动势接近母线电压，电压裕量不足';
    if (emf.Ke_at_speed < Vdc * 0.2) emfCheck = '⚠️ 反电动势偏低，电机出力可能不足';

    const Vdc = params.Vdc || 48;

    const lines = [
        '',
        '╔══════════════════════════════════════════════════════════╗',
        '║           电机设计参数计算报告                           ║',
        '╠══════════════════════════════════════════════════════════╣',
        '║  基本参数                                               ║',
        `║    极数/极对数    ${String(poles).padEnd(6)} / ${String(ps.p).padEnd(6)}                          ║`,
        `║    槽数/相数      ${String(slots).padEnd(6)} / ${String(phases).padEnd(6)}                          ║`,
        `║    频率/同步转速  ${String(freq+'Hz').padEnd(6)} / ${String(emf.n_sync+'rpm').padEnd(6)}                      ║`,
        `║    额定转速       ${String(speed+' rpm').padEnd(20)}                        ║`,
        '╠══════════════════════════════════════════════════════════╣',
        '║  极槽配合                                               ║',
        `║    每极每相槽数 q = ${ps.q.toFixed(2).padEnd(18)}                     ║`,
        `║    绕组类型       ${ps.slotType.padEnd(32)}   ║`,
        `║    节距           ${String(y+'槽 (短距'+Math.round(ps.shortPitchRatio*100)+'%)').padEnd(32)}   ║`,
        `║    分布系数 Kd    ${ps.kd.toFixed(4).padEnd(32)}   ║`,
        `║    绕组系数 Kw    ${ps.kw.toFixed(4).padEnd(32)}   ║`,
        '╠══════════════════════════════════════════════════════════╣',
        '║  磁路参数                                               ║',
        `║    定子内径/铁长  ${String(boreDiameter+' / '+coreLength+' mm').padEnd(32)}   ║`,
        `║    气隙长度       ${String(airGap+' mm').padEnd(32)}   ║`,
        `║    极距 τ         ${String(fd.tau.toFixed(2)+' mm').padEnd(32)}   ║`,
        `║    气隙磁密 Bg    ${String(fd.Bg.toFixed(4)+' T').padEnd(32)}   ║`,
        `║    齿部磁密 Bt    ${String(fd.B_t.toFixed(4)+' T').padEnd(32)}   ║`,
        `║    轭部磁密 By    ${String(fd.B_y.toFixed(4)+' T').padEnd(32)}   ║`,
        `║    每极磁通 Φg    ${String(fd.Phi_g.toFixed(4)+' mWb').padEnd(32)}   ║`,
        '╠══════════════════════════════════════════════════════════╣',
        '║  绕组与性能                                               ║',
        `║    每槽导体数     ${String(Ns+' 根').padEnd(32)}   ║`,
        `║    并联支路数     ${String(a+' 路').padEnd(32)}   ║`,
        `║    每相串联匝数   ${String(emf.Nph.toFixed(0)+' 匝').padEnd(32)}   ║`,
        `║    反电动势 Ke    ${String(emf.Ke_at_speed.toFixed(1)+' V（线间@'+speed+'rpm）').padEnd(32)}   ║`,
        `║    转矩常数 Kt    ${String(emf.Kt.toFixed(4)+' Nm/A').padEnd(32)}   ║`,
        '╠══════════════════════════════════════════════════════════╣',
        '║  功率估算（参考）                                         ║',
        `║    电流密度 Jc    ${String(power.Jc.toFixed(1)+' A/mm²').padEnd(32)}   ║`,
        `║    估算功率       ${String(power.P_mech.toFixed(0)+' W').padEnd(32)}   ║`,
        `║    估算转矩       ${String(power.T_out.toFixed(2)+' Nm').padEnd(32)}   ║`,
        `║    效率（估）     ${String((power.efficiency*100).toFixed(0)+'%').padEnd(32)}   ║`,
        '╠══════════════════════════════════════════════════════════╣',
        '║  合理性检查                                               ║',
        `║    ${magCheck.padEnd(48).substring(0,48)}  ║`,
        `║    ${emfCheck.padEnd(48).substring(0,48)}  ║`,
        `║    ${cogging.level.padEnd(48).substring(0,48)}  ║`,
        '╚══════════════════════════════════════════════════════════╝',
        ''
    ];

    return lines.join('\n');
}

// ============================================================
// 极槽配合方案对比
// ============================================================

function compareSlotOptions(poles = 8, baseParams = {}) {
    const options = [
        { slots: 24, q: 24/(8*3), name: '24槽(q=1)' },
        { slots: 36, q: 36/(8*3), name: '36槽(q=1.5)' },
        { slots: 48, q: 48/(8*3), name: '48槽(q=2)' },
        { slots: 54, q: 54/(8*3), name: '54槽(q=2.25)' },
    ];

    console.log('\n═══════════════════════════════════════════════════════');
    console.log('           极槽配合方案对比（极数=8）');
    console.log('═══════════════════════════════════════════════════════');
    console.log(' Q     q        Kw       Bg(T)    Ke(V)    特点');
    console.log('────────────────────────────────────────────────────');

    for (const opt of options) {
        const ps = calculatePoleSlot(poles, opt.slots, 3);
        const emf = calculateEMF({...baseParams, slots: opt.slots, kw: ps.kw});
        console.log(
            `${String(opt.slots).padEnd(4)} ` +
            `${String(ps.q.toFixed(2)).padEnd(6)} ` +
            `${ps.kw.toFixed(4).padEnd(9)} ` +
            `${emf.Phi_g > 0 ? (emf.Phi_g*1e6/157).toFixed(4) : 'N/A'.padEnd(7)} ` +
            `${emf.Ke_at_speed.toFixed(1).padEnd(7)} ` +
            `${opt.name}`
        );
    }
    console.log('═══════════════════════════════════════════════════════\n');
}

// ============================================================
// 交互模式
// ============================================================

function interactiveMode() {
    const readline = require('readline');
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

    const question = (q) => new Promise(r => rl.question(q, r));

    (async () => {
        console.log('\n╔═══════════════════════════════════════╗');
        console.log('║     电机设计参数计算器 v2（交互模式）   ║');
        console.log('╚═══════════════════════════════════════╝\n');

        const poles   = parseInt(await question('极数 (8): ') || '8');
        const slots    = parseInt(await question('槽数 (36): ') || '36');
        const freq     = parseInt(await question('频率 Hz (50): ') || '50');
        const speed    = parseInt(await question('额定转速 rpm (3000): ') || '3000');
        const boreD    = parseFloat(await question('定子内径 mm (54): ') || '54');
        const coreL    = parseFloat(await question('铁心长度 mm (60): ') || '60');
        const airGap   = parseFloat(await question('气隙长度 mm (0.5): ') || '0.5');
        const Br       = parseFloat(await question('永磁体Br T (1.25): ') || '1.25');
        const Ns       = parseInt(await question('每槽导体数 (28): ') || '28');
        const a        = parseInt(await question('并联支路数 (2): ') || '2');
        const Vdc      = parseFloat(await question('母线电压 V (48): ') || '48');

        rl.close();

        const params = { poles, slots, freq, speed, boreDiameter: boreD,
                         coreLength: coreL, airGap, Br, Ns, a, Vdc };

        console.log(generateReport(params));
        compareSlotOptions(poles, params);
    })();
}

// ============================================================
// 主入口
// ============================================================

function main() {
    const args = process.argv.slice(2);

    if (args.includes('--interactive') || args.includes('-i')) {
        interactiveMode();
        return;
    }

    if (args.includes('--compare_slots')) {
        const params = parseArgs(args);
        compareSlotOptions(params.poles || 8, params);
        return;
    }

    const params = parseArgs(args);
    console.log(generateReport(params));
}

function parseArgs(args) {
    const result = {};
    for (const arg of args) {
        const [key, value] = arg.split('=');
        if (value === undefined) continue;
        const num = parseFloat(value);
        result[key] = isNaN(num) ? value : num;
    }
    return result;
}

if (require.main === module) {
    main();
}

module.exports = { calculatePoleSlot, calculateFluxDensity, calculateEMF,
                   estimateCoggingTorque, generateReport, compareSlotOptions };
