import { useState, useEffect, useMemo } from 'react';
import { AnimatePresence, motion, useReducedMotion } from 'motion/react';
import { 
  ArrowUpRight,
  Download,
  Shield, 
  Activity, 
  Database, 
  Network, 
  Search,
  Bell,
  Settings,
  Clock,
  Users,
  FileCheck,
  X
} from 'lucide-react';
import watchdogMascotLogo from '../assets/watchdog-mascot-transparent.png';

const DIMENSION_ORDER = ['heartbeat','standards','memory','cron','shared','comm','security'];
const DIMENSION_CN: Record<string, string> = {
  heartbeat: '运行心跳',
  standards: '能力规范',
  memory: '记忆安全',
  cron: '定时任务',
  shared: '共享空间',
  comm: '连接边界',
  security: '防护基线',
};
const DIMENSION_EN: Record<string, string> = {
  heartbeat: '会不会偷懒',
  standards: '会不会跑偏',
  memory: '会不会记错',
  cron: '会不会漏事',
  shared: '大家同不同步',
  comm: '消息通不通',
  security: '会不会失控',
};
const DIMENSION_SHORT: Record<string, string> = {
  heartbeat: '心跳',
  standards: '规范',
  memory: '记忆',
  cron: '定时',
  shared: '共享',
  comm: '连接',
  security: '安全',
};
const INTERACTIVE_DIMENSIONS = new Set(DIMENSION_ORDER);
const RAW_JSON_DOWNLOADS = [
  { key: 'heartbeat', label: '运行心跳 JSON', filename: 'latest_heartbeat.json' },
  { key: 'standards', label: '能力规范 JSON', filename: 'latest_standards.json' },
  { key: 'memory', label: '记忆安全 JSON', filename: 'latest_memory.json' },
  { key: 'cron', label: '定时任务 JSON', filename: 'latest_cron.json' },
  { key: 'shared', label: '共享空间 JSON', filename: 'latest_shared.json' },
  { key: 'comm', label: '连接边界 JSON', filename: 'latest_comm.json' },
  { key: 'security', label: '防护基线 JSON', filename: 'latest_security.json' },
];

const DIM_ICONS: Record<string, any> = {
  heartbeat: Activity, standards: FileCheck, memory: Database,
  cron: Clock, shared: Users, comm: Network, security: Shield,
};

function getWatchdogData(): any {
  return (window as any).__WATCHDOG_DATA__ || null;
}

function downloadJsonFile(filename: string, data: any) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

function getRawJsonHref(filename: string): string {
  return new URL(filename, window.location.href).toString();
}

function fmtBool(v: boolean | undefined | null): string {
  if (v === true) return '是';
  if (v === false) return '否';
  return '—';
}

function asArray(v: any): string[] {
  if (Array.isArray(v)) return v.map((x) => String(x));
  return [];
}

function asText(v: any): string {
  if (v === null || v === undefined || v === '') return '—';
  if (typeof v === 'boolean') return v ? '是' : '否';
  if (typeof v === 'object') return JSON.stringify(v);
  return String(v);
}

function getDimIssueCount(dim: any, level: 'HIGH' | 'MEDIUM' | 'LOW'): number {
  return Number(dim?.issue_counts?.[level] ?? 0);
}

function WatchdogMascotLogo() {
  const reduceMotion = useReducedMotion();
  return (
    <motion.div
      className="relative h-full w-full shrink-0"
      animate={reduceMotion ? { scale: 1 } : { y: [0, -2, 0], rotate: [-0.8, 0.8, -0.8], scale: [1, 1.01, 1] }}
      transition={{ duration: 4.6, repeat: Infinity, ease: 'easeInOut' }}
    >
      <motion.div
        className="absolute inset-3 rounded-full bg-rose-500/20 blur-xl"
        animate={reduceMotion ? { opacity: 0.2 } : { scale: [1, 1.08, 1], opacity: [0.18, 0.34, 0.18] }}
        transition={{ duration: 3.6, repeat: Infinity, ease: 'easeInOut' }}
      />

      <motion.div
        className="absolute inset-[12px] rounded-full border border-cyan-300/12"
        animate={reduceMotion ? { opacity: 0.14 } : { opacity: [0.1, 0.2, 0.1], scale: [0.985, 1.015, 0.985] }}
        transition={{ duration: 3.8, repeat: Infinity, ease: 'easeInOut' }}
      />

      <motion.div
        className="absolute inset-0"
        animate={reduceMotion ? { scale: 1 } : { scale: [1, 1.01, 1], y: [0, -1, 0] }}
        transition={{ duration: 3.4, repeat: Infinity, ease: 'easeInOut' }}
      >
        <img
          src={watchdogMascotLogo}
          alt="Watchdog mascot"
          className="h-full w-full object-contain drop-shadow-[0_14px_28px_rgba(239,68,68,0.28)]"
        />
      </motion.div>

      <motion.div
        className="absolute left-1/2 top-[6px] h-[14px] w-[14px] -translate-x-1/2 rounded-full bg-slate-100/35 blur-[4px]"
        animate={reduceMotion ? { opacity: 0.18 } : { opacity: [0.12, 0.34, 0.12], scale: [0.92, 1.08, 0.92] }}
        transition={{ duration: 3.6, repeat: Infinity, ease: 'easeInOut' }}
      />
      <motion.div
        className="absolute left-[20px] top-[10px] h-8 w-2 rounded-full bg-white/30 blur-[2px]"
        animate={reduceMotion ? { opacity: 0 } : { opacity: [0, 0.45, 0], x: [0, 10, 20] }}
        transition={{ duration: 4.2, repeat: Infinity, ease: 'easeInOut', repeatDelay: 1.4 }}
      />

      <motion.div
        className="absolute bottom-[10px] left-1/2 h-3 w-7 -translate-x-1/2 rounded-full bg-cyan-400/8 blur-md"
        animate={reduceMotion ? { opacity: 0.08 } : { opacity: [0.08, 0.16, 0.08], scaleX: [0.98, 1.04, 0.98] }}
        transition={{ duration: 3.6, repeat: Infinity, ease: 'easeInOut' }}
      />
    </motion.div>
  );
}

export default function App() {
  const reduceMotion = useReducedMotion();
  const wd = useMemo(() => getWatchdogData(), []);
  const gs = wd?.global_score ?? 92;
  const [securityScore] = useState(gs);
  const [selectedDimension, setSelectedDimension] = useState<string | null>(null);
  const stats = wd?.stats || {};
  const dims = wd?.dimensions || {};
  const botInfo = wd?.bot_info || {};
  const selectedDim = selectedDimension ? dims[selectedDimension] : null;

  return (
    <div className="min-h-screen w-full bg-[#050510] flex items-center justify-center p-8 overflow-hidden relative">
      {/* Enhanced background with mesh gradient */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Mesh gradient background */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-indigo-900/20 via-transparent to-transparent" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,_var(--tw-gradient-stops))] from-purple-900/20 via-transparent to-transparent" />
        
        {/* Animated orbs */}
        <motion.div
          className="absolute top-[10%] right-[15%] w-[520px] h-[520px] rounded-full"
          style={{
            background: 'radial-gradient(circle, rgba(99, 102, 241, 0.12) 0%, transparent 70%)',
            filter: 'blur(60px)',
          }}
          animate={reduceMotion ? { opacity: 0.14 } : { y: [0, 28, 0], x: [0, 18, 0], scale: [1, 1.06, 1] }}
          transition={{
            duration: 16,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <motion.div
          className="absolute bottom-[10%] left-[15%] w-[440px] h-[440px] rounded-full"
          style={{
            background: 'radial-gradient(circle, rgba(139, 92, 246, 0.12) 0%, transparent 70%)',
            filter: 'blur(60px)',
          }}
          animate={reduceMotion ? { opacity: 0.12 } : { y: [0, -24, 0], x: [0, -16, 0], scale: [1, 1.08, 1] }}
          transition={{
            duration: 14,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        <motion.div
          className="absolute top-[50%] left-[50%] w-[320px] h-[320px] rounded-full"
          style={{
            background: 'radial-gradient(circle, rgba(168, 85, 247, 0.08) 0%, transparent 70%)',
            filter: 'blur(50px)',
          }}
          animate={reduceMotion ? { opacity: 0.1 } : { rotate: [0, 360], scale: [1, 1.08, 1] }}
          transition={{
            duration: 28,
            repeat: Infinity,
            ease: "linear"
          }}
        />
        
        {/* Grid overlay */}
        <div className="absolute inset-0 opacity-[0.02]"
          style={{
            backgroundImage: `linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                             linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)`,
            backgroundSize: '50px 50px',
          }}
        />
      </div>

      <div className="max-w-[1400px] w-full relative z-10">
        {/* Header */}
        <Header score={securityScore} botInfo={botInfo} watchdogData={wd} />

        {/* Main Dashboard Grid */}
        <motion.div 
          className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          {/* Left Panel - Threat Vectors */}
          <ThreatVectorsCard />

          {/* Center Panel - Main Score */}
          <MainScoreCard score={securityScore} />

          {/* Right Panel - Metrics Grid */}
          <MetricsGrid />
        </motion.div>

        {/* Bottom Row - Status Cards */}
        <motion.div 
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-7 gap-4 mt-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          {DIMENSION_ORDER.map((key) => {
            const dim = dims[key];
            return (
              <StatusCard
                key={key}
                Icon={DIM_ICONS[key] || Shield}
                dimensionKey={key}
                label={DIMENSION_CN[key]}
                subtitle={DIMENSION_EN[key]}
                score={dim?.status === 'active' ? (dim?.score ?? 100) : null}
                issueCounts={dim?.issue_counts || {}}
                fixedCount={Number(dim?.resolved_count ?? 0)}
                metadata={dim?.metadata || {}}
                issues={dim?.issues || []}
                onOpenDetail={() => {
                  if (INTERACTIVE_DIMENSIONS.has(key)) {
                    setSelectedDimension(key);
                  }
                }}
              />
            );
          })}
        </motion.div>

        {/* Alert Cards */}
        <AlertsSection />
      </div>

      <AnimatePresence>
        {selectedDimension && selectedDim && INTERACTIVE_DIMENSIONS.has(selectedDimension) && (
          <StatusDrawer
            dimensionKey={selectedDimension}
            label={DIMENSION_CN[selectedDimension]}
            subtitle={DIMENSION_EN[selectedDimension]}
            dimension={selectedDim}
            onClose={() => setSelectedDimension(null)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

function getBotInitials(name: string): string {
  if (!name) return 'OC';
  const trimmed = name.trim();
  if (/^[a-zA-Z\s]+$/.test(trimmed)) {
    return trimmed.split(/\s+/).filter(Boolean).slice(0, 2).map(w => w[0].toUpperCase()).join('');
  }
  return [...trimmed].slice(0, 2).join('');
}

function BotAvatar({ botInfo }: { botInfo: { bot_name?: string; avatar_url?: string } }) {
  const name = botInfo?.bot_name || '';
  const avatarUrl = botInfo?.avatar_url || '';
  if (avatarUrl) {
    return (
      <img
        src={avatarUrl}
        alt={name}
        className="w-full h-full object-cover rounded-full"
        onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
      />
    );
  }
  return <span className="text-sm font-bold text-white">{getBotInitials(name)}</span>;
}

function Header({ score, botInfo, watchdogData }: { score: number; botInfo: { bot_name?: string; avatar_url?: string }; watchdogData: any }) {
  const [showDownloads, setShowDownloads] = useState(false);
  const [comingSoonNotice, setComingSoonNotice] = useState<string | null>(null);

  useEffect(() => {
    if (!comingSoonNotice) return;
    const timer = window.setTimeout(() => setComingSoonNotice(null), 1800);
    return () => window.clearTimeout(timer);
  }, [comingSoonNotice]);

  const showComingSoon = () => {
    setShowDownloads(false);
    setComingSoonNotice('敬请后续升级，敬请期待');
  };

  return (
    <motion.header 
      className="relative z-30 flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <div className="flex items-center gap-5 lg:gap-6">
        <motion.div
          className="relative h-[86px] w-[86px] shrink-0"
          whileHover={{ scale: 1.05, rotate: -2 }}
          transition={{ type: "spring", stiffness: 320 }}
        >
          <WatchdogMascotLogo />
        </motion.div>

        <div className="flex flex-col justify-center">
          <div className="flex flex-wrap items-baseline gap-x-3">
            <h1 className="text-[32px] font-bold leading-none tracking-[-0.02em] text-white sm:text-[36px]">
              OPENCLAW
            </h1>
            <span className="text-[32px] font-bold leading-none tracking-[-0.02em] text-[#88A9FF] sm:text-[36px]">
              安全卫士
            </span>
          </div>

          <p className="mt-2.5 text-[15px] font-medium text-slate-300/90 tracking-wide">
            openclaw-watchdog / 妈妈再也不担心我养龙虾了
            <span className="ml-1.5 align-[1px] text-lg">🦞</span>
          </p>
        </div>
      </div>
      <div className="relative z-40 flex items-center gap-3 self-start lg:self-auto">
        <motion.div 
          className="rounded-full border border-[#88A9FF]/25 bg-[#88A9FF]/10 px-4 py-2 backdrop-blur-sm"
          whileHover={{ scale: 1.04, borderColor: 'rgba(136, 169, 255, 0.45)' }}
        >
          <span className="text-sm text-slate-200">健康度: <span className="font-mono text-[#BFD0FF]">{score}%</span></span>
        </motion.div>
        <div className="relative z-50">
          <motion.button
            type="button"
            className="w-10 h-10 rounded-full bg-white/5 backdrop-blur-sm border border-white/10 flex items-center justify-center group relative overflow-hidden"
            whileHover={{ scale: 1.06, borderColor: 'rgba(34,211,238,0.28)' }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setShowDownloads((v) => !v)}
          >
            <motion.div
              className="absolute inset-0 bg-cyan-500/14 opacity-0 group-hover:opacity-100 transition-opacity"
            />
            <Download className="w-4 h-4 text-gray-400 group-hover:text-cyan-200 transition-colors relative z-10" />
          </motion.button>
          {showDownloads && (
            <div className="absolute right-0 top-full z-[70] mt-3 w-72 rounded-2xl border border-cyan-400/20 bg-[#0b1022]/95 p-3 shadow-2xl backdrop-blur-xl">
              <div className="text-xs font-semibold tracking-[0.18em] text-cyan-200/80">JSON 下载</div>
              <button
                type="button"
                className="mt-3 w-full rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-left text-sm text-white transition hover:border-cyan-400/30 hover:bg-white/10"
                onClick={() => downloadJsonFile('latest_status.json', watchdogData)}
              >
                下载完整结果 `latest_status.json`
              </button>
              <div className="mt-3 text-xs text-slate-400">维度原始日志</div>
              <div className="mt-2 space-y-2">
                {RAW_JSON_DOWNLOADS.map((item) => (
                  <a
                    key={item.filename}
                    href={getRawJsonHref(item.filename)}
                    download={item.filename}
                    className="block rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-sm text-slate-200 transition hover:border-cyan-400/30 hover:bg-white/10"
                  >
                    {item.label}
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
        <motion.button 
          type="button"
          className="w-10 h-10 rounded-full bg-white/5 backdrop-blur-sm border border-white/10 flex items-center justify-center group relative overflow-hidden"
          whileHover={{ scale: 1.06, borderColor: 'rgba(103, 232, 249, 0.28)' }}
          whileTap={{ scale: 0.95 }}
          onClick={showComingSoon}
          title="敬请后续升级，敬请期待"
        >
          <motion.div
            className="absolute inset-0 bg-cyan-500/14 opacity-0 group-hover:opacity-100 transition-opacity"
          />
          <Search className="w-4 h-4 text-gray-400 group-hover:text-cyan-200 transition-colors relative z-10" />
        </motion.button>
        <motion.button 
          type="button"
          className="w-10 h-10 rounded-full bg-white/5 backdrop-blur-sm border border-white/10 flex items-center justify-center group relative overflow-hidden"
          whileHover={{ scale: 1.06, borderColor: 'rgba(129, 140, 248, 0.28)' }}
          whileTap={{ scale: 0.95 }}
          onClick={showComingSoon}
          title="敬请后续升级，敬请期待"
        >
          <motion.div
            className="absolute inset-0 bg-indigo-500/14 opacity-0 group-hover:opacity-100 transition-opacity"
          />
          <Bell className="w-4 h-4 text-gray-400 group-hover:text-indigo-200 transition-colors relative z-10" />
          <motion.div
            className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-cyan-400/90 rounded-full border-2 border-[#050510]"
            animate={{ opacity: [0.7, 1, 0.7] }}
            transition={{ duration: 2.4, repeat: Infinity }}
          />
        </motion.button>
        <motion.button 
          type="button"
          className="w-10 h-10 rounded-full bg-white/5 backdrop-blur-sm border border-white/10 flex items-center justify-center group relative overflow-hidden"
          whileHover={{ scale: 1.06, rotate: 16, borderColor: 'rgba(167, 139, 250, 0.28)' }}
          whileTap={{ scale: 0.95 }}
          transition={{ type: "spring", stiffness: 400 }}
          onClick={showComingSoon}
          title="敬请后续升级，敬请期待"
        >
          <motion.div
            className="absolute inset-0 bg-violet-500/14 opacity-0 group-hover:opacity-100 transition-opacity"
          />
          <Settings className="w-4 h-4 text-gray-400 group-hover:text-violet-300 transition-colors relative z-10" />
        </motion.button>
        <motion.div
          className="w-10 h-10 rounded-full bg-gradient-to-br from-sky-500 via-indigo-500 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/25 cursor-pointer overflow-hidden"
          whileHover={{ scale: 1.06, rotate: 4 }}
          whileTap={{ scale: 0.95 }}
          title={botInfo?.bot_name || 'OpenClaw'}
        >
          <BotAvatar botInfo={botInfo} />
        </motion.div>
        <AnimatePresence>
          {comingSoonNotice && (
            <motion.div
              className="absolute right-14 top-full z-[80] mt-3 rounded-2xl border border-violet-400/20 bg-[#0b1022]/95 px-4 py-3 text-sm text-slate-100 shadow-2xl backdrop-blur-xl"
              initial={{ opacity: 0, y: -8, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -6, scale: 0.98 }}
              transition={{ duration: 0.18 }}
            >
              {comingSoonNotice}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.header>
  );
}

function ThreatVectorsCard() {
  return (
    <motion.div
      className="relative group"
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.6, delay: 0.3 }}
      whileHover={{ y: -5 }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      <div className="relative backdrop-blur-xl bg-white/5 rounded-2xl border border-white/10 p-6 shadow-2xl overflow-hidden">
        {/* Animated gradient overlay */}
        <motion.div 
          className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 via-transparent to-blue-500/5"
          animate={{
            opacity: [0.3, 0.5, 0.3],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-base font-semibold text-white tracking-wide">七维健康雷达</h3>
            <div className="px-3 py-2 rounded-lg bg-cyan-500/10 border border-cyan-500/20">
              <div className="flex items-center gap-2 text-xs text-gray-300">
                <span className="inline-block w-2 h-2 rounded-full bg-yellow-300" />
                <span>本次扫描</span>
              </div>
              <div className="flex items-center gap-2 text-xs text-gray-300 mt-1">
                <span className="inline-block w-2 h-2 rounded-full bg-cyan-400" />
                <span>过去 30 天平均</span>
              </div>
            </div>
          </div>

          {/* Radar Chart */}
          <div className="relative h-[320px] flex items-center justify-center mb-6">
            <RadarChart />
          </div>

          {/* Status */}
          <div className="flex items-center justify-between pt-4 border-t border-white/5">
            <span className="text-sm text-gray-400">综合评估</span>
            <motion.span 
              className="text-sm font-bold text-cyan-400"
              animate={{ opacity: [0.7, 1, 0.7] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              稳定
            </motion.span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

function RadarChart() {
  const wd = getWatchdogData();
  const dims = wd?.dimensions || {};
  const avg30 = wd?.radar_avg_30d || {};
  const activeDims = DIMENSION_ORDER.filter(k => dims[k]?.status === 'active');
  const angleStep = activeDims.length > 0 ? 360 / activeDims.length : 51;
  const points = activeDims.map((k, i) => ({
    key: k,
    label: DIMENSION_CN[k] || k,
    shortLabel: DIMENSION_SHORT[k] || (DIMENSION_CN[k] || k),
    angle: i * angleStep,
    value: (dims[k]?.score ?? 80) / 100,
  }));
  const avgPoints = activeDims.map((k, i) => ({
    key: k,
    label: DIMENSION_CN[k] || k,
    angle: i * angleStep,
    value: (avg30[k] ?? dims[k]?.score ?? 80) / 100,
  }));

  const radius = 80;
  const center = 120;

  const getPoint = (angle: number, distance: number) => {
    const rad = (angle - 90) * Math.PI / 180;
    return {
      x: center + Math.cos(rad) * distance,
      y: center + Math.sin(rad) * distance,
    };
  };

  const dataPoints = points.map(p => getPoint(p.angle, p.value * radius));
  const avgDataPoints = avgPoints.map(p => getPoint(p.angle, p.value * radius));
  const pathData = dataPoints.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ') + ' Z';
  const avgPathData = avgDataPoints.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ') + ' Z';

  return (
    <div className="w-full flex flex-col items-center">
      <svg width="240" height="240" className="absolute inset-0">
      {/* Grid circles */}
      {[0.2, 0.4, 0.6, 0.8, 1].map((scale, i) => (
        <motion.circle
          key={i}
          cx={center}
          cy={center}
          r={radius * scale}
          fill="none"
          stroke="rgba(255,255,255,0.05)"
          strokeWidth="1"
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: i * 0.1, duration: 0.5 }}
        />
      ))}

      {/* Grid lines */}
      {points.map((point, i) => {
        const endPoint = getPoint(point.angle, radius);
        return (
          <motion.line
            key={i}
            x1={center}
            y1={center}
            x2={endPoint.x}
            y2={endPoint.y}
            stroke="rgba(255,255,255,0.05)"
            strokeWidth="1"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ delay: i * 0.1, duration: 0.5 }}
          />
        );
      })}

      {/* Data polygon */}
      <motion.path
        d={pathData}
        fill="rgba(250, 204, 21, 0.18)"
        stroke="rgba(250, 204, 21, 0.9)"
        strokeWidth="2"
        strokeDasharray="4 4"
        initial={{ opacity: 0, scale: 0 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.5, duration: 0.8 }}
      />
      <motion.path
        d={avgPathData}
        fill="rgba(6, 182, 212, 0.12)"
        stroke="rgba(6, 182, 212, 0.8)"
        strokeWidth="2"
        strokeDasharray="2 6"
        initial={{ opacity: 0, scale: 0 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.5, duration: 0.8 }}
      />

      {/* Data points */}
      {dataPoints.map((point, i) => (
        <motion.circle
          key={i}
          cx={point.x}
          cy={point.y}
          r="4"
          fill="#facc15"
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.7 + i * 0.05, duration: 0.3 }}
          whileHover={{ scale: 1.5, r: 6 }}
        />
      ))}

      {/* Labels */}
      {points.map((point, i) => {
        const labelPoint = getPoint(point.angle, radius + 25);
        return (
          <motion.text
            key={i}
            x={labelPoint.x}
            y={labelPoint.y}
            fill={point.value > 0.7 ? '#06b6d4' : 'rgba(255,255,255,0.4)'}
            fontSize="12"
            textAnchor="middle"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 + i * 0.05 }}
          >
            {point.shortLabel}
          </motion.text>
        );
      })}
      </svg>
      <div className="grid grid-cols-2 gap-x-4 gap-y-1 mt-56 w-full text-xs text-gray-300">
        {points.map((point, i) => (
          <div key={point.key} className="flex items-center justify-between">
            <span>{point.label}</span>
            <span className="font-mono text-gray-200">{Math.round(point.value * 100)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function MainScoreCard({ score }: { score: number }) {
  const reduceMotion = useReducedMotion();
  const wd = getWatchdogData();
  const genAt = (wd?.generated_at || '').slice(0,19).replace('T',' ');
  const s = wd?.stats || {};
  const activeCount = DIMENSION_ORDER.filter((k) => wd?.dimensions?.[k]?.status === 'active').length;
  const severityTone =
    score >= 85
      ? 'text-emerald-300 border-emerald-400/25 bg-emerald-500/10'
      : score >= 70
        ? 'text-cyan-300 border-cyan-400/25 bg-cyan-500/10'
        : score >= 50
          ? 'text-amber-300 border-amber-400/25 bg-amber-500/10'
          : 'text-rose-300 border-rose-400/25 bg-rose-500/10';

  return (
    <motion.div
      className="relative group flex h-full cursor-pointer flex-col"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.6, delay: 0.4 }}
      whileHover={{ y: -5 }}
    >
      <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-500/20 blur-xl opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
      <div className="relative h-full overflow-hidden rounded-2xl border border-white/10 bg-[linear-gradient(180deg,rgba(9,12,28,0.92),rgba(6,8,22,0.82))] p-8 shadow-2xl backdrop-blur-xl">
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 via-transparent to-blue-500/5"
          animate={reduceMotion ? { opacity: 0.28 } : { opacity: [0.24, 0.42, 0.24] }}
          transition={{ duration: 3.8, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          className="absolute -left-12 top-6 h-40 w-40 rounded-full bg-cyan-500/10 blur-3xl"
          animate={reduceMotion ? { opacity: 0.18 } : { x: [0, 12, 0], y: [0, 8, 0], opacity: [0.18, 0.28, 0.18] }}
          transition={{ duration: 9.5, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          className="absolute -right-10 bottom-8 h-44 w-44 rounded-full bg-violet-500/14 blur-3xl"
          animate={reduceMotion ? { opacity: 0.16 } : { x: [0, -10, 0], y: [0, -8, 0], opacity: [0.16, 0.26, 0.16] }}
          transition={{ duration: 8.8, repeat: Infinity, ease: 'easeInOut' }}
        />
        <motion.div
          className="absolute inset-x-10 top-0 h-px bg-gradient-to-r from-transparent via-cyan-300/50 to-transparent"
          animate={reduceMotion ? { opacity: 0.2 } : { opacity: [0.12, 0.35, 0.12] }}
          transition={{ duration: 3.6, repeat: Infinity, ease: 'easeInOut' }}
        />

        <div className="relative z-10 flex h-full flex-col items-center justify-center">
          <div className="relative mb-7 h-72 w-72">
            <motion.div
              className="absolute inset-0 rounded-full border border-cyan-400/16"
              animate={reduceMotion ? { scale: 1 } : { rotate: 360, scale: [1, 1.012, 1] }}
              transition={{ rotate: { duration: 24, repeat: Infinity, ease: 'linear' }, scale: { duration: 6, repeat: Infinity, ease: 'easeInOut' } }}
            />
            <motion.div
              className="absolute inset-[12px] rounded-full border border-dashed border-violet-400/18"
              animate={reduceMotion ? { rotate: 0 } : { rotate: -360 }}
              transition={{ duration: 32, repeat: Infinity, ease: 'linear' }}
            />
            <motion.div
              className="absolute inset-[28px] rounded-full border border-white/8"
              animate={reduceMotion ? { opacity: 0.36 } : { scale: [1, 1.028, 1], opacity: [0.26, 0.5, 0.26] }}
              transition={{ duration: 5.2, repeat: Infinity, ease: 'easeInOut' }}
            />
            <motion.div
              className="absolute inset-[20px] rounded-full border border-cyan-300/0 opacity-0 transition-all duration-300 group-hover:border-cyan-300/20 group-hover:opacity-100"
              animate={reduceMotion ? { opacity: 0.18 } : { scale: [1, 1.035, 1], opacity: [0.14, 0.28, 0.14] }}
              transition={{ duration: 3.2, repeat: Infinity, ease: 'easeInOut' }}
            />

            <motion.div
              className="absolute left-1/2 top-1/2 h-[168px] w-[168px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-[radial-gradient(circle_at_30%_30%,rgba(125,211,252,0.35),rgba(79,70,229,0.18)_32%,rgba(15,23,42,0.95)_72%)] shadow-[0_0_70px_rgba(99,102,241,0.22)]"
              animate={reduceMotion ? { boxShadow: '0 0 55px rgba(99,102,241,0.18)' } : { scale: [1, 1.02, 1], boxShadow: ['0 0 55px rgba(99,102,241,0.18)', '0 0 76px rgba(34,211,238,0.22)', '0 0 55px rgba(99,102,241,0.18)'] }}
              transition={{ duration: 4.8, repeat: Infinity, ease: 'easeInOut' }}
              whileHover={{ scale: 1.05 }}
            >
              <div className="absolute inset-[10px] rounded-full border border-white/10 bg-[linear-gradient(180deg,rgba(15,23,42,0.58),rgba(2,6,23,0.82))] backdrop-blur-md" />
              <motion.div
                className="absolute left-1/2 top-[14px] h-10 w-3 -translate-x-1/2 rounded-full bg-white/40 blur-[3px]"
                animate={reduceMotion ? { opacity: 0 } : { opacity: [0, 0.55, 0], x: [-6, 0, 8] }}
                transition={{ duration: 4.2, repeat: Infinity, ease: 'easeInOut', repeatDelay: 1.2 }}
              />
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <motion.div
                  className="min-w-[132px] bg-gradient-to-b from-white via-cyan-100 to-violet-200 bg-clip-text px-[0.06em] text-center text-[82px] font-black leading-none tracking-[-0.03em] text-transparent"
                  animate={reduceMotion ? { scale: 1 } : { scale: [1, 1.018, 1] }}
                  transition={{ duration: 3.8, repeat: Infinity, ease: 'easeInOut' }}
                  style={{ textShadow: '0 0 30px rgba(125,211,252,0.18)' }}
                >
                  {score}
                </motion.div>
                <div className="mt-1 text-[12px] font-medium uppercase tracking-[0.38em] text-slate-300/78">
                  健康指数
                </div>
              </div>
            </motion.div>

            {[
              { label: `${activeCount}/7 在线`, cls: 'left-0 top-[34px] text-cyan-200 border-cyan-400/20 bg-cyan-500/10', motionCls: { x: [-6, 0], opacity: [0, 1] } },
              { label: `${s.current_open ?? 0} 待处理`, cls: 'right-0 top-[50px] text-violet-200 border-violet-400/20 bg-violet-500/10', motionCls: { x: [6, 0], opacity: [0, 1] } },
              { label: `${s.total_resolved ?? 0} 已修复`, cls: 'left-[14px] bottom-[34px] text-emerald-200 border-emerald-400/20 bg-emerald-500/10', motionCls: { y: [8, 0], opacity: [0, 1] } },
              { label: '悬浮查看细节', cls: 'right-[10px] bottom-[28px] text-amber-200 border-amber-400/20 bg-amber-500/10', motionCls: { y: [8, 0], opacity: [0, 1] } },
            ].map((chip, i) => (
              <motion.div
                key={chip.label}
                className={`absolute rounded-full border px-3 py-1 text-[11px] tracking-wide backdrop-blur-md ${chip.cls} opacity-0 group-hover:opacity-100`}
                animate={chip.motionCls}
                transition={{ duration: 0.35, delay: 0.05 * i }}
              >
                {chip.label}
              </motion.div>
            ))}

            {[...Array(6)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute left-1/2 top-1/2 h-1.5 w-1.5 rounded-full bg-cyan-300/75 shadow-[0_0_14px_rgba(103,232,249,0.8)]"
                animate={reduceMotion ? { opacity: 0.18, scale: 0.6 } : {
                  x: [0, Math.cos((i * 60) * Math.PI / 180) * 112],
                  y: [0, Math.sin((i * 60) * Math.PI / 180) * 112],
                  opacity: [0, 0.75, 0],
                  scale: [0.2, 1, 0.2],
                }}
                transition={{
                  duration: 3.8,
                  repeat: Infinity,
                  delay: i * 0.28,
                  ease: 'easeOut',
                }}
              />
            ))}
          </div>

          <motion.div 
            className="text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
          >
            <div className={`mx-auto mb-3 inline-flex rounded-full border px-3 py-1 text-[11px] tracking-[0.22em] ${severityTone}`}>
              {score >= 85 ? '稳定' : score >= 70 ? '活跃' : score >= 50 ? '观察' : '高危'}
            </div>
            <h3 className="mb-1.5 text-lg font-semibold text-white">
              {score >= 85 ? '系统运行正常' : score >= 70 ? '基本健康，有轻微风险' : score >= 50 ? '存在待处理问题' : '需要立即关注'}
            </h3>
            <p className="text-xs text-slate-500">
              最近扫描: <span className="font-mono text-slate-400">{genAt || '—'}</span>
            </p>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
}

function MetricsGrid() {
  const wd = getWatchdogData();
  const s = wd?.stats || {};
  const dims = wd?.dimensions || {};
  const activeCount = DIMENSION_ORDER.filter(k => dims[k]?.status === 'active').length;
  const metrics = [
    { label: '累计发现', value: String(s.total_discovered ?? 24), change: `+${s.current_open ?? 3}`, trend: 'up', color: 'cyan', bars: [40, 60, 50, 80, 90] },
    { label: '已修复', value: String(s.total_resolved ?? 18), status: s.total_discovered ? `${Math.round((s.total_resolved/s.total_discovered)*100)}%` : '—', color: 'blue', bars: [20, 25, 15, 30, 20] },
    { label: '待处理', value: String(s.current_open ?? 6), status: (s.current_open ?? 0) > 0 ? '关注中' : '已清零', color: 'emerald', bars: [10, 12, 8, 10, 15] },
    { label: '监控维度', value: `${activeCount}/7`, status: activeCount >= 7 ? '全部在线' : '部分在线', color: 'violet', bars: [95, 96, 97, 98, 99] },
  ];

  return (
    <motion.div
      className="relative group"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.6, delay: 0.5 }}
      whileHover={{ y: -5 }}
    >
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/18 to-indigo-500/18 rounded-2xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
      <div className="relative backdrop-blur-xl bg-white/5 rounded-2xl border border-white/10 p-6 shadow-2xl">
        <div className="grid grid-cols-2 gap-4">
          {metrics.map((metric, index) => (
            <MetricCard key={index} metric={metric} index={index} />
          ))}
        </div>
      </div>
    </motion.div>
  );
}

function MetricCard({ metric, index }: { metric: any; index: number }) {
  const colorMap: any = {
    cyan: { bg: 'from-cyan-500/20 to-cyan-600/20', border: 'border-cyan-500/30', text: 'text-cyan-400', bar: 'bg-cyan-500' },
    blue: { bg: 'from-blue-500/20 to-blue-600/20', border: 'border-blue-500/30', text: 'text-blue-400', bar: 'bg-blue-500' },
    emerald: { bg: 'from-emerald-500/20 to-emerald-600/20', border: 'border-emerald-500/30', text: 'text-emerald-400', bar: 'bg-emerald-500' },
    violet: { bg: 'from-violet-500/20 to-violet-600/20', border: 'border-violet-500/30', text: 'text-violet-400', bar: 'bg-violet-500' },
  };

  const colors = colorMap[metric.color];

  return (
    <motion.div
      className={`relative backdrop-blur-sm bg-gradient-to-br ${colors.bg} rounded-xl border ${colors.border} p-4 overflow-hidden group/card`}
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.6 + index * 0.1, duration: 0.4 }}
      whileHover={{ scale: 1.02, y: -2 }}
    >
      {/* Animated background gradient */}
      <motion.div 
        className="absolute inset-0 opacity-0 group-hover/card:opacity-100 transition-opacity"
        animate={{
          background: [
            'radial-gradient(circle at 0% 0%, rgba(255,255,255,0.05) 0%, transparent 50%)',
            'radial-gradient(circle at 100% 100%, rgba(255,255,255,0.05) 0%, transparent 50%)',
            'radial-gradient(circle at 0% 0%, rgba(255,255,255,0.05) 0%, transparent 50%)',
          ],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "linear"
        }}
      />

      <div className="relative z-10">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <motion.div 
            className="flex items-center gap-2"
            whileHover={{ x: 2 }}
          >
            <div className={`w-5 h-5 rounded ${colors.bar} opacity-20 flex items-center justify-center`}>
              <div className={`w-2 h-2 rounded-full ${colors.bar}`} />
            </div>
            {metric.change && (
              <span className={`text-xs ${colors.text}`}><span className="font-mono">{metric.change}</span></span>
            )}
            {metric.status && (
              <span className="text-xs text-gray-300">{metric.status}</span>
            )}
          </motion.div>
        </div>

        {/* Label */}
        <div className="text-sm text-gray-400 mb-1">
          {metric.label}
        </div>

        {/* Value */}
        <div className="text-2xl font-bold text-white mb-3">
          {metric.value}
        </div>

        {/* Bar chart */}
        <div className="flex items-end gap-1 h-6">
          {metric.bars.map((height: number, i: number) => (
            <motion.div
              key={i}
              className={`flex-1 ${colors.bar} rounded-t opacity-50`}
              initial={{ height: 0 }}
              animate={{ height: `${height}%` }}
              transition={{
                delay: 0.8 + index * 0.1 + i * 0.05,
                duration: 0.4,
                ease: "easeOut"
              }}
              whileHover={{ opacity: 1, height: `${Math.min(height * 1.1, 100)}%` }}
            />
          ))}
        </div>
      </div>
    </motion.div>
  );
}

function getMetadataSections(dimensionKey: string, metadata: any): { title: string; rows?: [string, string][]; bullets?: string[] }[] {
  if (!metadata) return [];
  if (dimensionKey === 'heartbeat') {
    const lightOn = asArray(metadata?.light_context?.on);
    const lightOff = asArray(metadata?.light_context?.off);
    const tokenMap = metadata?.heartbeat_md_tokens || {};
    const tokenValues = Object.values(tokenMap).map((x) => Number(x || 0));
    const maxTokens = tokenValues.length ? Math.max(...tokenValues) : 0;
    const activeHours = metadata?.active_hours ? Object.values(metadata.active_hours).join(' / ') : '24x7';
    const modelCost = asText(metadata?.model_cost_level);
    return [
      {
        title: '龙虾有多勤快',
        rows: [
          ['主动巡检数', asText(metadata?.active_heartbeats)],
          ['平均多久看一次', `${asText(metadata?.avg_interval_min)} 分钟`],
          ['一天大概看几次', asText(metadata?.daily_calls_est)],
        ],
      },
      {
        title: '它靠什么脑子在跑',
        rows: [
          ['默认模型', asText(metadata?.default_model)],
          ['成本体感', modelCost],
          ['成本提示', asText(metadata?.cost_hint)],
        ],
      },
      {
        title: '是不是轻装上阵',
        rows: [
          ['lightContext 状态', lightOff.length > 0 ? '部分启用' : (lightOn.length > 0 ? '已启用' : '未启用')],
          ['HEARTBEAT 大小', `${maxTokens || 0} tokens (${maxTokens > 1000 ? '偏大' : '正常'})`],
        ],
      },
      {
        title: '什么时候会看你',
        rows: [
          ['活跃时段', String(activeHours || '24x7')],
          ['静默时段', asText(metadata?.quiet_hours || '无')],
        ],
      },
    ];
  }
  if (dimensionKey === 'standards') {
    const fileStatuses = metadata?.file_statuses || {};
    const soulEntries = Object.entries(fileStatuses).filter(([k]) => k.endsWith('/SOUL.md')) as [string, any][];
    const agentsEntries = Object.entries(fileStatuses).filter(([k]) => k.endsWith('/AGENTS.md')) as [string, any][];
    const soulLatest = soulEntries.map(([, v]) => v).sort((a, b) => String(b.last_modified || '').localeCompare(String(a.last_modified || '')))[0];
    const agentsLatest = agentsEntries.map(([, v]) => v).sort((a, b) => String(b.last_modified || '').localeCompare(String(a.last_modified || '')))[0];
    const soulOk = soulEntries.every(([, v]) => String(v?.check || '').toUpperCase() === 'OK');
    const coverAll = agentsEntries.every(([, v]) => Boolean(v?.covers_all_agents));
    return [
      {
        title: '它知不知道自己是谁',
        rows: [
          ['SOUL 最近状态', `${asText(soulLatest?.last_modified)} · ${soulOk ? '完整' : '缺少 section'}`],
          ['AGENTS 最近状态', `${asText(agentsLatest?.last_modified)} · 覆盖全部 agent：${coverAll ? '是' : '否'}`],
        ],
      },
      {
        title: '该会的本事有没有写清',
        rows: [
          ['能力清单', asText(metadata?.capability_lists)],
          ['公司基线', asText(metadata?.company_baseline)],
        ],
      },
      {
        title: '你需要留意的地方',
        bullets: asArray(metadata?.risk_hints).slice(0, 3),
      },
    ];
  }
  if (dimensionKey === 'memory') {
    return [
      {
        title: '它记了多少旧事',
        rows: [
          ['记忆份数', asText(metadata?.sessions)],
          ['陈旧占比', asText(metadata?.stale_sessions)],
        ],
      },
      {
        title: '有没有记到不该记的',
        rows: [['敏感命中', asText(metadata?.sensitive_hits)]],
      },
      {
        title: '这些记忆怎么留',
        rows: [['保留策略', asText(metadata?.retention_policy)]],
      },
    ];
  }
  if (dimensionKey === 'cron') {
    const recent = asArray(metadata?.recent_jobs).length > 0
      ? (metadata?.recent_jobs as any[]).slice(0, 3).map((j) => `${asText(j?.name)} · 最近状态：${asText(j?.status)}（${asText(j?.last_run)}）`)
      : [];
    return [
      {
        title: '该做的事有没有真的在跑',
        rows: [
          ['启用任务', asText(metadata?.jobs_configured)],
          ['近 24h 运行次数', asText(metadata?.last_24h_runs)],
          ['失败率', asText(metadata?.failure_rate)],
        ],
      },
      {
        title: '最近最活跃的任务（前3条）',
        bullets: recent,
      },
    ];
  }
  if (dimensionKey === 'shared') {
    return [
      {
        title: '大家是不是看同一本账',
        rows: [
          ['共享层启用', fmtBool(Boolean(metadata?.enabled))],
          ['共享资料体积', asText(metadata?.size)],
        ],
      },
      {
        title: '里面主要放了什么',
        rows: [['主要文件类型', asText(metadata?.file_types)]],
      },
      {
        title: '有没有混入危险东西',
        rows: [
          ['权限状态', asText(metadata?.permissions)],
          ['敏感配置', Number(metadata?.sensitive_config ?? 0) > 0 ? `是（${metadata?.sensitive_config}）` : '否'],
        ],
      },
    ];
  }
  if (dimensionKey === 'comm') {
    return [
      {
        title: '消息链路通不通',
        rows: [
          ['在线通道数', asText(metadata?.channels_active)],
          ['当前通道', asArray(metadata?.channel_list).join(' · ') || '—'],
        ],
      },
      {
        title: '会不会突然失联',
        rows: [['即将过期', asText(metadata?.tokens_expiring_soon)]],
      },
      {
        title: '对外怎么发',
        rows: [['出网策略', asText(metadata?.outbound_policy)]],
      },
    ];
  }
  if (dimensionKey === 'security') {
    return [
      {
        title: '龙虾有没有刹车',
        rows: [
          ['Exec 白名单', fmtBool(Boolean(metadata?.exec_approvals_enabled))],
          ['通配放行', fmtBool(Boolean(metadata?.wildcard_rules))],
          ['自动放行技能', asText(metadata?.auto_allow_skills)],
        ],
      },
      {
        title: '敏感信息安不安全',
        rows: [
          ['高权限密钥', asText(metadata?.high_privilege_keys)],
          ['泄露模式', asText(metadata?.leaked_patterns)],
        ],
      },
      {
        title: '现在最该担心什么',
        bullets: asArray(metadata?.risk_summary).slice(0, 3),
      },
    ];
  }
  return [];
}

function getScoreTone(score: number | null): string {
  if (score === null) return 'text-gray-300';
  if (score >= 85) return 'text-emerald-300';
  if (score >= 70) return 'text-cyan-300';
  if (score >= 50) return 'text-amber-300';
  return 'text-red-300';
}

function getIssueSeveritySummary(issueCounts: any): string {
  const total = getDimIssueCount({ issue_counts: issueCounts }, 'HIGH')
    + getDimIssueCount({ issue_counts: issueCounts }, 'MEDIUM')
    + getDimIssueCount({ issue_counts: issueCounts }, 'LOW');
  if (total === 0) return '当前无告警';
  return `当前 ${total} 个告警`;
}

function formatStatusLabel(status: string): string {
  switch (status) {
    case 'idle':
      return '最近成功';
    case 'running':
      return '执行中';
    case 'disabled':
      return '已禁用';
    case 'corrupted':
      return '记录损坏';
    case 'unknown':
      return '未知';
    default:
      return status || '未知';
  }
}

function getStatusTone(status: string): string {
  switch (status) {
    case 'idle':
      return 'border-emerald-400/25 bg-emerald-500/10 text-emerald-200';
    case 'running':
      return 'border-cyan-400/25 bg-cyan-500/10 text-cyan-200';
    case 'disabled':
      return 'border-slate-400/25 bg-slate-500/10 text-slate-200';
    case 'corrupted':
      return 'border-red-400/25 bg-red-500/10 text-red-200';
    default:
      return 'border-amber-400/25 bg-amber-500/10 text-amber-200';
  }
}

function formatRunAt(value: string): string {
  if (!value) return '未运行';
  return String(value).replace('T', ' ').replace(/(\.\d+)?([+-]\d\d:\d\d|Z)?$/, '');
}

function formatSchedule(schedule: any): string {
  if (!schedule || typeof schedule !== 'object') return '未配置';
  if (schedule.kind === 'cron') {
    return `${schedule.expr || '—'} · ${schedule.tz || '未设时区'}`;
  }
  if (schedule.kind === 'at') {
    return `一次性 · ${schedule.at || '未设时间'}`;
  }
  return `${schedule.kind || '未知'} · ${schedule.expr || schedule.at || '未配置'}`;
}

function getCardSummary(dimensionKey: string, metadata: any, issueCounts: any): { headline: string; detail: string } {
  if (dimensionKey === 'cron') {
    const jobsConfigured = Number(metadata?.jobs_configured ?? 0);
    const lastRuns = Number(metadata?.last_24h_runs ?? 0);
    const disabled = Number(metadata?.jobs_disabled ?? 0);
    return {
      headline: `有 ${jobsConfigured} 件定时事在托管`,
      detail: `过去 24h 跑了 ${lastRuns} 次，${getIssueSeveritySummary(issueCounts)}，停用 ${disabled} 个`,
    };
  }
  if (dimensionKey === 'heartbeat') {
    const active = Number(metadata?.active_heartbeats ?? 0);
    const avgInterval = Number(metadata?.avg_interval_min ?? 0);
    return {
      headline: `${active} 个主动巡检在盯着龙虾`,
      detail: `平均 ${avgInterval || 0} 分钟看一次，${getIssueSeveritySummary(issueCounts)}`,
    };
  }
  if (dimensionKey === 'standards') {
    return {
      headline: '龙虾知道自己是谁、该做什么',
      detail: `${getIssueSeveritySummary(issueCounts)}，能力清单 ${asText(metadata?.capability_lists)}，基线 ${asText(metadata?.company_baseline)}`,
    };
  }
  if (dimensionKey === 'memory') {
    return {
      headline: '它还记得住人和上下文',
      detail: `${asText(metadata?.sessions)} 份记忆，${getIssueSeveritySummary(issueCounts)}，敏感命中 ${asText(metadata?.sensitive_hits)}`,
    };
  }
  if (dimensionKey === 'shared') {
    return {
      headline: '团队共识有没有放在同一本账上',
      detail: `${getIssueSeveritySummary(issueCounts)}，共享层${fmtBool(Boolean(metadata?.enabled)) === '是' ? '已启用' : '未启用'}，权限 ${asText(metadata?.permissions)}`,
    };
  }
  if (dimensionKey === 'comm') {
    return {
      headline: '该发的消息有没有路可走',
      detail: `${asText(metadata?.channels_active)} 条通道在线，${getIssueSeveritySummary(issueCounts)}，即将过期 ${asText(metadata?.tokens_expiring_soon)}`,
    };
  }
  if (dimensionKey === 'security') {
    return {
      headline: '先防误发，再防越权失控',
      detail: `${getIssueSeveritySummary(issueCounts)}，Exec 白名单 ${fmtBool(Boolean(metadata?.exec_approvals_enabled))}，高权限密钥 ${asText(metadata?.high_privilege_keys)}`,
    };
  }
  return {
    headline: getIssueSeveritySummary(issueCounts),
    detail: '点击查看完整详情',
  };
}

function DrawerMetric({ label, value, tone = 'text-white' }: { label: string; value: string; tone?: string }) {
  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-4">
      <div className="text-xs text-gray-400">{label}</div>
      <div className={`mt-2 text-lg font-semibold ${tone}`}>{value}</div>
    </div>
  );
}

function ActionPanel({
  title,
  actions,
}: {
  title: string;
  actions: string[];
}) {
  if (actions.length === 0) return null;
  return (
    <section className="space-y-3">
      <div>
        <div className="text-lg font-semibold text-white">{title}</div>
        <div className="mt-1 text-sm text-slate-400">这里给的是建议顺序，不是强制执行。</div>
      </div>
      <div className="rounded-2xl border border-cyan-400/15 bg-cyan-500/5 p-4">
        <ul className="space-y-2">
          {actions.map((action, idx) => (
            <li key={idx} className="text-sm leading-relaxed text-slate-200">
              {idx + 1}. {action}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

function ClampText({
  children,
  className,
  lines,
}: {
  children: string;
  className?: string;
  lines: number;
}) {
  return (
    <div
      className={className}
      style={{
        display: '-webkit-box',
        WebkitLineClamp: lines,
        WebkitBoxOrient: 'vertical',
        overflow: 'hidden',
      }}
    >
      {children}
    </div>
  );
}

function StatusCard({
  Icon,
  dimensionKey,
  label,
  subtitle,
  score,
  issueCounts,
  fixedCount,
  metadata,
  issues,
  onOpenDetail,
}: any) {
  const high = getDimIssueCount({ issue_counts: issueCounts }, 'HIGH');
  const med = getDimIssueCount({ issue_counts: issueCounts }, 'MEDIUM');
  const low = getDimIssueCount({ issue_counts: issueCounts }, 'LOW');
  const isDisabled = score === null || score === undefined;
  const scoreTone = getScoreTone(isDisabled ? null : Number(score));
  const isInteractive = INTERACTIVE_DIMENSIONS.has(dimensionKey);
  const cardSummary = getCardSummary(dimensionKey, metadata, issueCounts);

  return (
    <motion.button
      type="button"
      onClick={isInteractive ? onOpenDetail : undefined}
      className={`relative h-[220px] w-full overflow-hidden rounded-xl border border-slate-600/40 bg-gradient-to-br from-slate-900/70 to-slate-800/60 p-4 text-left shadow-lg group/status ${isInteractive ? 'cursor-pointer' : 'cursor-default'}`}
      whileHover={{ y: -3, scale: 1.01 }}
      transition={{ type: "spring", stiffness: 380 }}
    >
      <div className="relative z-10 flex h-full flex-col">
        <div className="flex items-start justify-between">
          <div>
            <div className="text-sm font-semibold text-white">{label}</div>
            <div className="text-xs text-gray-400">{subtitle}</div>
          </div>
          <Icon className="w-5 h-5 text-slate-200" strokeWidth={2.2} />
        </div>

        <div className="mt-3 flex items-end justify-between">
          <div className={`text-3xl font-bold ${scoreTone}`}>{isDisabled ? '—' : score}</div>
          <div className="text-xs text-gray-400">{isDisabled ? '未启用' : '得分'}</div>
        </div>

        <div className="mt-3 flex items-center gap-2 text-xs text-gray-300">
          <span className="text-red-300">H <span className="font-mono">{high}</span></span>
          <span className="text-amber-300">M <span className="font-mono">{med}</span></span>
          <span className="text-cyan-300">L <span className="font-mono">{low}</span></span>
          <span className="ml-auto text-emerald-300"><span className="font-mono">{fixedCount}</span> 已修复</span>
        </div>

        <div className="mt-4 min-h-[46px]">
          <ClampText lines={2} className="text-sm leading-relaxed text-slate-300">
            {cardSummary.headline}
          </ClampText>
        </div>

        <div className="mt-auto pt-3" />
      </div>
      {isInteractive && (
        <div className="pointer-events-none absolute inset-x-3 bottom-3 z-20 translate-y-2 rounded-lg border border-cyan-400/20 bg-[linear-gradient(180deg,rgba(14,116,144,0.14),rgba(14,116,144,0.06))] px-3 py-2 opacity-0 shadow-[0_10px_25px_rgba(34,211,238,0.08)] backdrop-blur-md transition-all duration-200 group-hover/status:translate-y-0 group-hover/status:opacity-100">
          <div className="flex items-center justify-between text-[11px] text-cyan-200">
            <span>点击查看详情</span>
            <ArrowUpRight className="h-3.5 w-3.5" />
          </div>
        </div>
      )}
    </motion.button>
  );
}

function StatusDrawer({ dimensionKey, label, subtitle, dimension, onClose }: any) {
  const metadata = dimension?.metadata || {};
  const issues = dimension?.issues || [];
  const issueCounts = dimension?.issue_counts || {};
  const high = getDimIssueCount({ issue_counts: issueCounts }, 'HIGH');
  const med = getDimIssueCount({ issue_counts: issueCounts }, 'MEDIUM');
  const low = getDimIssueCount({ issue_counts: issueCounts }, 'LOW');

  return (
    <>
      <motion.button
        type="button"
        className="fixed inset-0 z-40 bg-slate-950/72 backdrop-blur-[2px]"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      />
      <motion.aside
        className="fixed right-0 top-0 z-50 h-full w-full max-w-[760px] overflow-hidden border-l border-cyan-400/20 bg-[linear-gradient(180deg,rgba(8,11,28,0.98),rgba(5,8,22,0.98))] shadow-2xl"
        initial={{ x: '100%' }}
        animate={{ x: 0 }}
        exit={{ x: '100%' }}
        transition={{ type: 'spring', stiffness: 280, damping: 28 }}
      >
        <div className="flex h-full flex-col">
          <div className="border-b border-white/10 px-6 py-5">
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="text-xs tracking-[0.22em] text-cyan-200/80">维度详情</div>
                <div className="mt-2 text-2xl font-semibold text-white">{label}</div>
                <div className="mt-1 text-sm text-slate-400">{subtitle}</div>
                <div className="mt-3 flex flex-wrap gap-2 text-xs">
                  <span className="rounded-full border border-red-400/20 bg-red-500/10 px-2.5 py-1 text-red-200">高风险 {high}</span>
                  <span className="rounded-full border border-amber-400/20 bg-amber-500/10 px-2.5 py-1 text-amber-200">中风险 {med}</span>
                  <span className="rounded-full border border-cyan-400/20 bg-cyan-500/10 px-2.5 py-1 text-cyan-200">低风险 {low}</span>
                </div>
              </div>
              <button
                type="button"
                onClick={onClose}
                className="rounded-full border border-white/10 bg-white/5 p-2 text-slate-300 transition hover:border-cyan-400/30 hover:text-white"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto px-6 py-5">
            {dimensionKey === 'cron' && <CronDrawerContent metadata={metadata} issues={issues} />}
            {dimensionKey === 'heartbeat' && <HeartbeatDrawerContent metadata={metadata} issues={issues} />}
            {!['cron', 'heartbeat'].includes(dimensionKey) && (
              <GenericDrawerContent dimensionKey={dimensionKey} metadata={metadata} issues={issues} />
            )}
          </div>
        </div>
      </motion.aside>
    </>
  );
}

function CronDrawerContent({ metadata, issues }: { metadata: any; issues: any[] }) {
  const jobs = Array.isArray(metadata?.job_catalog) ? metadata.job_catalog : [];
  const riskJobs = jobs.filter((job: any) =>
    job?.lastStatus === 'running' ||
    Number(job?.consecutiveFailures ?? 0) > 0 ||
    (!job?.enabled) ||
    !job?.hasRunRecord
  );
  const actions = getRecommendedActions('cron', metadata, issues);

  return (
    <div className="space-y-6">
      <section>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <DrawerMetric label="启用任务数" value={String(metadata?.jobs_configured ?? 0)} tone="text-cyan-200" />
          <DrawerMetric label="禁用任务数" value={String(metadata?.jobs_disabled ?? 0)} tone="text-slate-200" />
          <DrawerMetric label="近 24h 运行次数" value={String(metadata?.last_24h_runs ?? 0)} tone="text-white" />
          <DrawerMetric label="近 24h 失败率" value={asText(metadata?.failure_rate)} tone="text-amber-200" />
        </div>
      </section>

      <ActionPanel title="建议动作" actions={actions} />

      <section className="space-y-3">
        <div>
          <div className="text-lg font-semibold text-white">任务清单</div>
          <div className="mt-1 text-sm text-slate-400">这里展示完整 cron 列表，不再只显示最近 3 条。</div>
        </div>
        <div className="space-y-3">
          {jobs.map((job: any) => (
            <div key={job.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <div className="text-base font-semibold text-white">{job.name || job.id}</div>
                  <div className="mt-1 font-mono text-xs text-slate-500">{job.id}</div>
                </div>
                <div className="flex flex-wrap gap-2 text-xs">
                  <span className={`rounded-full border px-2.5 py-1 ${getStatusTone(job.lastStatus)}`}>{formatStatusLabel(job.lastStatus)}</span>
                  <span className={`rounded-full border px-2.5 py-1 ${job.enabled ? 'border-cyan-400/20 bg-cyan-500/10 text-cyan-200' : 'border-slate-400/20 bg-slate-500/10 text-slate-200'}`}>
                    {job.enabled ? '已启用' : '已禁用'}
                  </span>
                </div>
              </div>

              <div className="mt-4 grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
                <div>
                  <div className="text-xs text-slate-400">调度表达式</div>
                  <div className="mt-1 text-slate-100">{formatSchedule(job.schedule)}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-400">运行位置</div>
                  <div className="mt-1 text-slate-100">{asText(job.sessionTarget)}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-400">投递模式</div>
                  <div className="mt-1 text-slate-100">{asText(job.deliveryMode)}</div>
                </div>
                <div>
                  <div className="text-xs text-slate-400">最近一次</div>
                  <div className="mt-1 text-slate-100">{asText(job.lastRunLabel)}{job.lastRun ? ` · ${formatRunAt(job.lastRun)}` : ''}</div>
                </div>
              </div>

              {Number(job?.consecutiveFailures ?? 0) > 0 && (
                <div className="mt-3 rounded-xl border border-red-400/20 bg-red-500/10 px-3 py-2 text-sm text-red-200">
                  连续失败 {job.consecutiveFailures} 次，需要优先排查。
                </div>
              )}
            </div>
          ))}
          {jobs.length === 0 && (
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-400">
              当前没有可展示的 cron 任务。
            </div>
          )}
        </div>
      </section>

      <section className="space-y-3">
        <div className="text-lg font-semibold text-white">当前风险</div>
        {issues.length > 0 ? (
          <div className="space-y-3">
            {issues.map((issue) => (
              <div key={issue.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div className="text-sm font-semibold text-white">{issue.title || issue.id}</div>
                  <span className={`rounded-full border px-2.5 py-1 text-xs ${issue.severity === 'HIGH' ? 'border-red-400/20 bg-red-500/10 text-red-200' : issue.severity === 'MEDIUM' ? 'border-amber-400/20 bg-amber-500/10 text-amber-200' : 'border-cyan-400/20 bg-cyan-500/10 text-cyan-200'}`}>
                    {issue.severity || 'LOW'}
                  </span>
                </div>
                <div className="mt-2 text-sm leading-relaxed text-slate-300">{issue.fix_action || issue.fix_command || '按工单建议处理。'}</div>
              </div>
            ))}
          </div>
        ) : (
          <div className="rounded-2xl border border-emerald-400/20 bg-emerald-500/10 p-4 text-sm text-emerald-200">
            当前没有定时任务告警。
          </div>
        )}

        {riskJobs.length > 0 && (
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="text-sm font-semibold text-white">需要重点关注的任务</div>
            <ul className="mt-3 space-y-2">
              {riskJobs.slice(0, 6).map((job: any) => (
                <li key={job.id} className="text-sm text-slate-300">
                  - {job.name || job.id}：{!job.enabled ? '已禁用' : !job.hasRunRecord ? '尚无运行记录' : job.lastStatus === 'running' ? '正在运行中' : `连续失败 ${job.consecutiveFailures} 次`}
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>
    </div>
  );
}

function HeartbeatDrawerContent({ metadata, issues }: { metadata: any; issues: any[] }) {
  const auditEntries = Object.entries(metadata?.execution_audit || {}) as [string, any][];
  const inactiveTemplates = asArray(metadata?.inactive_templates);
  const activeHours = metadata?.active_hours || {};
  const tokenMap = metadata?.heartbeat_md_tokens || {};
  const actions = getRecommendedActions('heartbeat', metadata, issues);

  return (
    <div className="space-y-6">
      <section>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
          <DrawerMetric label="启用 heartbeat 数" value={String(metadata?.active_heartbeats ?? 0)} tone="text-cyan-200" />
          <DrawerMetric label="平均间隔" value={`${asText(metadata?.avg_interval_min)} 分钟`} />
          <DrawerMetric label="估算日调用量" value={String(metadata?.daily_calls_est ?? 0)} />
          <DrawerMetric label="模型成本等级" value={asText(metadata?.model_cost_level)} tone="text-amber-200" />
        </div>
      </section>

      <ActionPanel title="建议动作" actions={actions} />

      <section className="space-y-3">
        <div>
          <div className="text-lg font-semibold text-white">心跳执行清单</div>
          <div className="mt-1 text-sm text-slate-400">直接看每个 agent 的执行边界，而不是英文 metadata 堆叠。</div>
        </div>
        <div className="space-y-3">
          {auditEntries.map(([agent, audit]) => {
            const agentHours = typeof activeHours === 'object' ? activeHours?.[agent] : activeHours;
            const toolBadges = [
              ['读文件', audit?.read_explicit],
              ['执行命令', audit?.exec_explicit],
              ['发消息', audit?.message_explicit],
              ['拉起会话', audit?.spawn_explicit],
            ] as [string, boolean][];

            return (
              <div key={agent} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <div className="text-base font-semibold text-white">{agent}</div>
                    <div className="mt-1 text-sm text-slate-400">
                      {audit?.lightContext ? 'lightContext' : '完整上下文'} · {asText(audit?.model)}
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 text-xs">
                    <span className={`rounded-full border px-2.5 py-1 ${audit?.substantive ? 'border-emerald-400/20 bg-emerald-500/10 text-emerald-200' : 'border-red-400/20 bg-red-500/10 text-red-200'}`}>
                      {audit?.substantive ? '有实质内容' : '缺少实质内容'}
                    </span>
                    <span className={`rounded-full border px-2.5 py-1 ${audit?.clear_silence_rule ? 'border-cyan-400/20 bg-cyan-500/10 text-cyan-200' : 'border-amber-400/20 bg-amber-500/10 text-amber-200'}`}>
                      {audit?.clear_silence_rule ? '沉默条件清晰' : '沉默条件不清'}
                    </span>
                  </div>
                </div>

                <div className="mt-4 grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
                  <div>
                    <div className="text-xs text-slate-400">活跃时段</div>
                    <div className="mt-1 text-slate-100">{asText(agentHours || '未配置（24x7）')}</div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-400">HEARTBEAT.md 体积</div>
                    <div className="mt-1 text-slate-100">{Number(tokenMap?.[agent] ?? 0)} tokens</div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-400">步骤数</div>
                    <div className="mt-1 text-slate-100">{asText(audit?.step_count)}</div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-400">外部依赖</div>
                    <div className="mt-1 text-slate-100">{Array.isArray(audit?.external_refs) ? audit.external_refs.length : 0} 个</div>
                  </div>
                </div>

                <div className="mt-4 flex flex-wrap gap-2">
                  {toolBadges.map(([text, enabled]) => (
                    <span
                      key={text}
                      className={`rounded-full border px-2.5 py-1 text-xs ${enabled ? 'border-cyan-400/20 bg-cyan-500/10 text-cyan-200' : 'border-slate-400/20 bg-slate-500/10 text-slate-300'}`}
                    >
                      {text} {enabled ? '已显式写出' : '未显式写出'}
                    </span>
                  ))}
                </div>

                {(asArray(audit?.time_logic_detected).length > 0 || asArray(audit?.unavailable_runtime_refs).length > 0) && (
                  <div className="mt-4 space-y-2 rounded-xl border border-amber-400/20 bg-amber-500/10 p-3 text-sm text-amber-100">
                    {asArray(audit?.time_logic_detected).length > 0 && (
                      <div>检测到时间逻辑：{asArray(audit?.time_logic_detected).join('、')}</div>
                    )}
                    {asArray(audit?.unavailable_runtime_refs).length > 0 && (
                      <div>检测到不可用运行时能力：{asArray(audit?.unavailable_runtime_refs).join('、')}</div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
          {auditEntries.length === 0 && (
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-400">
              当前没有可展示的心跳审计信息。
            </div>
          )}
        </div>
      </section>

      <section className="space-y-3">
        <div className="text-lg font-semibold text-white">当前风险</div>
        {issues.length > 0 ? (
          <div className="space-y-3">
            {issues.map((issue) => (
              <div key={issue.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div className="text-sm font-semibold text-white">{issue.title || issue.id}</div>
                  <span className={`rounded-full border px-2.5 py-1 text-xs ${issue.severity === 'HIGH' ? 'border-red-400/20 bg-red-500/10 text-red-200' : issue.severity === 'MEDIUM' ? 'border-amber-400/20 bg-amber-500/10 text-amber-200' : 'border-cyan-400/20 bg-cyan-500/10 text-cyan-200'}`}>
                    {issue.severity || 'LOW'}
                  </span>
                </div>
                <div className="mt-2 text-sm leading-relaxed text-slate-300">{issue.fix_action || issue.fix_command || '按工单建议处理。'}</div>
              </div>
            ))}
          </div>
        ) : (
          <div className="rounded-2xl border border-emerald-400/20 bg-emerald-500/10 p-4 text-sm text-emerald-200">
            当前没有运行心跳告警。
          </div>
        )}

        {inactiveTemplates.length > 0 && (
          <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
            <div className="text-sm font-semibold text-white">未启用但保留模板的 workspace</div>
            <div className="mt-2 text-sm text-slate-300">{inactiveTemplates.join('、')}</div>
          </div>
        )}
      </section>
    </div>
  );
}

function GenericDrawerContent({ dimensionKey, metadata, issues }: { dimensionKey: string; metadata: any; issues: any[] }) {
  const sections = getMetadataSections(dimensionKey, metadata);
  const metrics = getGenericDrawerMetrics(dimensionKey, metadata);
  const intro = getDrawerIntro(dimensionKey);
  const actions = getRecommendedActions(dimensionKey, metadata, issues);

  return (
    <div className="space-y-6">
      {metrics.length > 0 && (
        <section>
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {metrics.map((metric) => (
              <DrawerMetric key={metric.label} label={metric.label} value={metric.value} tone={metric.tone} />
            ))}
          </div>
        </section>
      )}

      <ActionPanel title="建议动作" actions={actions} />

      <section className="space-y-3">
        <div>
          <div className="text-lg font-semibold text-white">当前概况</div>
          <div className="mt-1 text-sm text-slate-400">{intro}</div>
        </div>
        <div className="space-y-3">
          {sections.map((sec, idx) => (
            <div key={idx} className="rounded-2xl border border-white/10 bg-white/5 p-4">
              <div className="mb-3 text-sm font-semibold text-white">{sec.title}</div>
              {sec.rows && (
                <div className="space-y-2">
                  {sec.rows.map(([k, v], ridx) => (
                    <div key={ridx} className="flex items-start justify-between gap-4 text-sm">
                      <span className="text-slate-400">{k}</span>
                      <span className="max-w-[60%] text-right text-slate-100">{v}</span>
                    </div>
                  ))}
                </div>
              )}
              {sec.bullets && sec.bullets.length > 0 && (
                <ul className="space-y-2">
                  {sec.bullets.map((b, bidx) => (
                    <li key={bidx} className="text-sm leading-relaxed text-slate-200">- {b}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
          {sections.length === 0 && (
            <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-slate-400">
              当前没有可展示的详情信息。
            </div>
          )}
        </div>
      </section>

      <section className="space-y-3">
        <div className="text-lg font-semibold text-white">当前风险</div>
        {issues.length > 0 ? (
          <div className="space-y-3">
            {issues.map((issue) => (
              <div key={issue.id} className="rounded-2xl border border-white/10 bg-white/5 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div className="text-sm font-semibold text-white">{issue.title || issue.id}</div>
                  <span className={`rounded-full border px-2.5 py-1 text-xs ${issue.severity === 'HIGH' ? 'border-red-400/20 bg-red-500/10 text-red-200' : issue.severity === 'MEDIUM' ? 'border-amber-400/20 bg-amber-500/10 text-amber-200' : 'border-cyan-400/20 bg-cyan-500/10 text-cyan-200'}`}>
                    {issue.severity || 'LOW'}
                  </span>
                </div>
                <div className="mt-2 text-sm leading-relaxed text-slate-300">{issue.fix_action || issue.fix_command || '按工单建议处理。'}</div>
              </div>
            ))}
          </div>
        ) : (
          <div className="rounded-2xl border border-emerald-400/20 bg-emerald-500/10 p-4 text-sm text-emerald-200">
            当前没有相关告警。
          </div>
        )}
      </section>
    </div>
  );
}

function getGenericDrawerMetrics(dimensionKey: string, metadata: any): { label: string; value: string; tone?: string }[] {
  if (dimensionKey === 'standards') {
    const fileStatuses = metadata?.file_statuses || {};
    const soulCount = Object.keys(fileStatuses).filter((k) => k.endsWith('/SOUL.md')).length;
    const agentCount = Object.keys(fileStatuses).filter((k) => k.endsWith('/AGENTS.md')).length;
    return [
      { label: 'SOUL 文件数', value: String(soulCount), tone: 'text-cyan-200' },
      { label: 'AGENTS 文件数', value: String(agentCount) },
      { label: '能力清单状态', value: asText(metadata?.capability_lists), tone: 'text-white' },
      { label: '公司基线', value: asText(metadata?.company_baseline), tone: asText(metadata?.company_baseline) === 'Pass' ? 'text-emerald-200' : 'text-amber-200' },
    ];
  }
  if (dimensionKey === 'memory') {
    return [
      { label: '会话数量', value: asText(metadata?.sessions), tone: 'text-cyan-200' },
      { label: '陈旧占比', value: asText(metadata?.stale_sessions) },
      { label: '敏感命中', value: asText(metadata?.sensitive_hits), tone: Number(metadata?.sensitive_hits ?? 0) > 0 ? 'text-amber-200' : 'text-emerald-200' },
      { label: '保留策略', value: asText(metadata?.retention_policy) },
    ];
  }
  if (dimensionKey === 'shared') {
    return [
      { label: '共享层启用', value: fmtBool(Boolean(metadata?.enabled)), tone: metadata?.enabled ? 'text-cyan-200' : 'text-slate-200' },
      { label: '目录体积', value: asText(metadata?.size) },
      { label: '文件类型', value: asText(metadata?.file_types) },
      { label: '敏感配置', value: Number(metadata?.sensitive_config ?? 0) > 0 ? `${metadata?.sensitive_config} 个` : '无', tone: Number(metadata?.sensitive_config ?? 0) > 0 ? 'text-amber-200' : 'text-emerald-200' },
    ];
  }
  if (dimensionKey === 'comm') {
    return [
      { label: '在线通道数', value: asText(metadata?.channels_active), tone: 'text-cyan-200' },
      { label: '通道列表', value: asArray(metadata?.channel_list).join('、') || '—' },
      { label: '即将过期', value: asText(metadata?.tokens_expiring_soon), tone: Number(metadata?.tokens_expiring_soon ?? 0) > 0 ? 'text-amber-200' : 'text-emerald-200' },
      { label: '出网策略', value: asText(metadata?.outbound_policy) },
    ];
  }
  if (dimensionKey === 'security') {
    return [
      { label: 'Exec 白名单', value: fmtBool(Boolean(metadata?.exec_approvals_enabled)), tone: metadata?.exec_approvals_enabled ? 'text-cyan-200' : 'text-amber-200' },
      { label: '通配规则', value: fmtBool(Boolean(metadata?.wildcard_rules)), tone: metadata?.wildcard_rules ? 'text-amber-200' : 'text-emerald-200' },
      { label: '高权限密钥', value: asText(metadata?.high_privilege_keys) },
      { label: '泄露模式', value: asText(metadata?.leaked_patterns), tone: Number(metadata?.leaked_patterns ?? 0) > 0 ? 'text-amber-200' : 'text-emerald-200' },
    ];
  }
  return [];
}

function getDrawerIntro(dimensionKey: string): string {
  if (dimensionKey === 'heartbeat') return '这项决定龙虾会不会主动看群、看数据、看任务。如果这里有问题，它可能不是偷懒，而是根本没被叫醒。';
  if (dimensionKey === 'standards') return '这项决定龙虾知不知道自己是谁、该帮你做什么。如果身份文件不清楚，它就容易答非所问、越做越偏。';
  if (dimensionKey === 'memory') return '这项决定龙虾会不会记错人、记混上下文、把旧事当新事。记忆越乱，后续回复越不靠谱。';
  if (dimensionKey === 'cron') return '这项决定那些该按点做的事会不会真的发生。日报、提醒、巡检看起来配好了，不代表真的有跑。';
  if (dimensionKey === 'shared') return '这项决定多只龙虾是不是在看同一份规则和目标。共享层乱了，大家就会各说各话，协作会越来越别扭。';
  if (dimensionKey === 'comm') return '这项决定龙虾能不能把消息、通知和协作真正送出去。通道挂了时，它可能以为自己做了，你却什么也收不到。';
  if (dimensionKey === 'security') return '这项决定龙虾会不会误碰高风险操作，或者把敏感信息暴露出去。安全做好了，自动化你才敢放心开。';
  return '这里展示这个维度和你养龙虾体验最相关的状态与风险。';
}

function getRecommendedActions(dimensionKey: string, metadata: any, issues: any[]): string[] {
  if (dimensionKey === 'heartbeat') {
    const actions: string[] = [];
    if (issues.length > 0) actions.push('先处理含时间逻辑、lightContext 自举不足、message 未显式写出的 heartbeat。');
    if (asArray(metadata?.inactive_templates).length > 0) actions.push(`核对这些模板是否仍需保留：${asArray(metadata?.inactive_templates).join('、')}。`);
    actions.push('若改了 HEARTBEAT.md 或 heartbeat 配置，按单 scanner -> 全 pipeline -> dashboard 的顺序做回归。');
    return actions;
  }
  if (dimensionKey === 'cron') {
    const jobs = Array.isArray(metadata?.job_catalog) ? metadata.job_catalog : [];
    const failing = jobs.filter((job: any) => Number(job?.consecutiveFailures ?? 0) > 0);
    const noRuns = jobs.filter((job: any) => job?.enabled && !job?.hasRunRecord);
    const actions: string[] = [];
    if (failing.length > 0) actions.push(`优先排查连续失败任务：${failing.slice(0, 3).map((job: any) => job.name || job.id).join('、')}。`);
    if (noRuns.length > 0) actions.push(`确认这些已启用任务为何尚无运行记录：${noRuns.slice(0, 3).map((job: any) => job.name || job.id).join('、')}。`);
    actions.push('改了 jobs.json 或调度策略后，至少重跑 cron -> aggregate -> dashboard 这一条链。');
    return actions;
  }
  if (dimensionKey === 'standards') {
    return issues.length > 0
      ? ['先补齐缺失的 SOUL/AGENTS section，再确认能力清单与公司基线是否一致。', '涉及 agent 身份文件时，修改后要重置对应 session。']
      : ['当前规范维度健康，后续新增 skill 或调整能力边界时，记得同步 AGENTS.md、SOUL.md、SKILLS-CATALOG。'];
  }
  if (dimensionKey === 'memory') {
    return issues.length > 0
      ? ['优先处理敏感信息、冲突事实和死链引用，再考虑会话归档。', '凡是权威事实冲突，先回到 shared/DECISIONS.md 或对应权威源核对。']
      : ['当前记忆维度健康，后续新增事实时优先写单一权威源，避免多处复制后漂移。'];
  }
  if (dimensionKey === 'shared') {
    return issues.length > 0
      ? ['先处理共享层缺挂载、权限过宽和敏感配置混入问题。', '共享层改动如果影响 OKR/DECISIONS/ROSTER，需要按规则重置所有相关 agent session。']
      : ['当前共享层状态正常，新增共享文件时尽量保持“少而关键”，不要把业务运行日志混进 shared。'];
  }
  if (dimensionKey === 'comm') {
    return issues.length > 0
      ? ['优先修复无效 spawn、缺失 binding 和即将过期的通道凭证。', '改通信路由后建议做一次真实消息链路冒烟，而不只看静态配置。']
      : ['当前通信路由健康，新增渠道或 agent binding 时同步检查 main/default 双账号覆盖。'];
  }
  if (dimensionKey === 'security') {
    return issues.length > 0
      ? ['优先处理高权限密钥、宽松白名单和历史泄露痕迹。', '涉及全局脚本或权限修复时，先用最小范围验证，再决定是否扩展到其它 skill。']
      : ['当前安全基线稳定，后续新增脚本入口时默认加路径白名单和权限检查。'];
  }
  return [];
}

function AlertsSection() {
  const wd = getWatchdogData();
  const issues = (wd?.active_issues || []) as any[];
  const [selectedId, setSelectedId] = useState<string | null>(issues[0]?.id || null);

  useEffect(() => {
    if (!issues.length) {
      setSelectedId(null);
      return;
    }
    if (!selectedId || !issues.some((i) => i.id === selectedId)) {
      setSelectedId(issues[0].id);
    }
  }, [issues, selectedId]);

  const selected = issues.find((i) => i.id === selectedId) || null;
  const sevBadge: Record<string, string> = {
    HIGH: 'bg-red-500/20 text-red-300 border-red-500/40',
    MEDIUM: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
    LOW: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/40',
  };

  return (
    <motion.div
      className="mt-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.6 }}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <h2 className="text-lg font-bold text-white">待处理问题</h2>
          <motion.div className="px-3 py-1 rounded-full bg-red-500/20 border border-red-500/30">
            <span className="text-xs text-red-300"><span className="font-mono">{issues.length}</span> 条进行中</span>
          </motion.div>
        </div>
      </div>

      {issues.length === 0 ? (
        <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 text-emerald-200 p-4 text-sm">
          当前没有待处理工单。
        </div>
      ) : (
        <div className="grid grid-cols-1 xl:grid-cols-[1.2fr_1fr] gap-4">
          <div className="rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm overflow-hidden">
            <div className="grid grid-cols-[100px_1fr_120px_80px] gap-3 px-4 py-3 text-xs text-gray-400 border-b border-white/10">
              <span>等级</span>
              <span>标题</span>
              <span>维度</span>
              <span>存活天数</span>
            </div>
            <div className="max-h-[360px] overflow-auto">
              {issues.map((issue) => {
                const selectedRow = issue.id === selectedId;
                return (
                  <button
                    key={issue.id}
                    onClick={() => setSelectedId(issue.id)}
                    className={`w-full grid grid-cols-[100px_1fr_120px_80px] gap-3 px-4 py-3 text-left border-b border-white/5 hover:bg-white/10 transition-colors ${selectedRow ? 'bg-white/10' : ''}`}
                  >
                    <span className={`inline-flex items-center justify-center rounded-md border text-xs px-2 py-1 ${sevBadge[issue.severity] || sevBadge.LOW}`}>
                      {issue.severity || 'LOW'}
                    </span>
                    <span className="text-sm text-white">{issue.title || issue.id}</span>
                    <span className="text-xs text-cyan-200">{DIMENSION_CN[issue.dimension] || issue.dimension}</span>
                    <span className="text-xs text-gray-300"><span className="font-mono">{issue.days_open || 0}</span>d</span>
                  </button>
                );
              })}
            </div>
          </div>

          <div className="rounded-xl border border-white/10 bg-white/5 backdrop-blur-sm p-4">
            <div className="text-sm font-semibold text-white mb-2">问题详情</div>
            {selected ? (
              <div className="space-y-3">
                <div className="rounded-lg bg-white/5 border border-white/10 p-3">
                  <div className="text-xs text-gray-400 mb-1">检查 ID</div>
                  <div className="text-sm text-cyan-200 font-mono break-all">{selected.id}</div>
                </div>
                <div className="rounded-lg bg-white/5 border border-white/10 p-3">
                  <div className="text-xs text-gray-400 mb-2">发现证据摘要</div>
                  <ul className="space-y-1">
                    {asArray(selected.evidence).slice(0, 3).map((item, idx) => (
                      <li key={idx} className="text-sm text-gray-200">- {item}</li>
                    ))}
                    {asArray(selected.evidence).length === 0 && <li className="text-sm text-gray-400">- 无证据摘要</li>}
                  </ul>
                </div>
                <div className="rounded-lg bg-white/5 border border-white/10 p-3">
                  <div className="text-xs text-gray-400 mb-1">建议修复动作（在飞书里执行）</div>
                  <div className="text-sm text-amber-200 leading-relaxed">{selected.fix_action || selected.fix_command || '请在飞书中按 SOP 处理该项风险。'}</div>
                </div>
              </div>
            ) : (
              <div className="text-sm text-gray-400">请选择一条工单查看详情。</div>
            )}
          </div>
        </div>
      )}
    </motion.div>
  );
}