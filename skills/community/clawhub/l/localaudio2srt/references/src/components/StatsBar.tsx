import React from 'react';
import { Box, Typography } from '@mui/material';
import Inventory2Icon from '@mui/icons-material/Inventory2';
import GraphicEqIcon from '@mui/icons-material/GraphicEq';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import TimerIcon from '@mui/icons-material/Timer';
import ModelTrainingIcon from '@mui/icons-material/ModelTraining';
import { useQueueStore } from '../store/queueStore';
import {
  formatDuration,
  formatEstimatedTime,
  getShortModelName,
} from '../utils/helpers';
import type { QueueStats } from '../types';

/** 统计项属性 */
interface StatItemProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  color: string;
}

/**
 * 单个统计项组件。
 */
const StatItem: React.FC<StatItemProps> = ({ icon, label, value, color }) => (
  <div
    className="flex items-center gap-2 px-3 py-1.5 rounded-lg"
    style={{ background: `${color}12` }}
  >
    <span style={{ color }}>{icon}</span>
    <Typography variant="caption" sx={{ color: '#9EA3B8', fontWeight: 500 }}>
      {label}
    </Typography>
    <Typography
      variant="body2"
      sx={{
        color,
        fontWeight: 800,
        fontSize: value.toString().length > 6 ? '0.75rem' : '1rem',
        minWidth: 20,
        textAlign: 'center',
      }}
    >
      {value}
    </Typography>
  </div>
);

/**
 * 统计面板组件 — 显示队列统计、模型名称、总时长和预估剩余时间。
 */
const StatsBar: React.FC = () => {
  const stats: QueueStats = useQueueStore((s) => s.getStats());
  const totalDuration = useQueueStore((s) => s.getTotalDuration());
  const estimatedRemaining = useQueueStore((s) => s.getEstimatedRemaining());
  const settings = useQueueStore((s) => s.settings);
  const defaultWhisperModelName = useQueueStore((s) => s.defaultWhisperModelName);
  const modelName = settings.modelPath
    ? getShortModelName(settings.modelPath)
    : defaultWhisperModelName || '默认';

  return (
    <Box
      sx={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: 1.5,
        py: 1.5,
        px: 0.5,
      }}
    >
      <StatItem
        icon={<Inventory2Icon sx={{ fontSize: 18 }} />}
        label="队列"
        value={stats.total}
        color="#9EA3B8"
      />
      <StatItem
        icon={<GraphicEqIcon sx={{ fontSize: 18 }} />}
        label="转录中"
        value={stats.transcribing + stats.loading}
        color="#7C4DFF"
      />
      <StatItem
        icon={<CheckCircleOutlineIcon sx={{ fontSize: 18 }} />}
        label="已完成"
        value={stats.completed}
        color="#4CAF50"
      />
      <StatItem
        icon={<ErrorOutlineIcon sx={{ fontSize: 18 }} />}
        label="失败"
        value={stats.failed}
        color="#F44336"
      />
      <StatItem
        icon={<ModelTrainingIcon sx={{ fontSize: 18 }} />}
        label="模型"
        value={modelName}
        color="#64B5F6"
      />
      <StatItem
        icon={<TimerIcon sx={{ fontSize: 18 }} />}
        label="总时长"
        value={formatDuration(totalDuration)}
        color="#FFB74D"
      />
      <StatItem
        icon={<TimerIcon sx={{ fontSize: 18 }} />}
        label="预计剩余"
        value={formatEstimatedTime(estimatedRemaining)}
        color="#CE93D8"
      />
    </Box>
  );
};

export default StatsBar;
