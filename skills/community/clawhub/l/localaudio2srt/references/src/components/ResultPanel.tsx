import React, { useState, useCallback } from 'react';
import {
  Box,
  Typography,
  Tabs,
  Tab,
  Button,
  IconButton,
  Tooltip,
  CircularProgress,
} from '@mui/material';
import TranslateIcon from '@mui/icons-material/Translate';
import SaveAltIcon from '@mui/icons-material/SaveAlt';
import CloseIcon from '@mui/icons-material/Close';
import SubtitlesIcon from '@mui/icons-material/Subtitles';
import TextFieldsIcon from '@mui/icons-material/TextFields';
import { useQueueStore } from '../store/queueStore';
import { exportSegmentsToSrt, formatSrtTime } from '../utils/helpers';
import type { SrtSegment } from '../types';

/**
 * 右侧转录结果面板 — 显示识别文本 / 翻译文本，支持翻译和导出 SRT。
 */
const ResultPanel: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0); // 0: 原文, 1: 译文
  const selectedTask = useQueueStore((s) => {
    if (!s.selectedTaskId) return undefined;
    return s.tasks.find((t) => t.id === s.selectedTaskId);
  });
  const translateTask = useQueueStore((s) => s.translateTask);
  const selectTask = useQueueStore((s) => s.selectTask);

  /** 点击翻译按钮 */
  const handleTranslate = useCallback(() => {
    if (selectedTask) {
      translateTask(selectedTask.id);
      setActiveTab(1); // 切换到翻译 Tab
    }
  }, [selectedTask, translateTask]);

  /** 导出 SRT 文件 */
  const handleSaveSrt = useCallback(
    (useTranslation: boolean) => {
      if (!selectedTask) return;
      const segments = useTranslation
        ? selectedTask.translatedSegments
        : selectedTask.segments;
      if (segments.length === 0) return;

      const srtContent = exportSegmentsToSrt(segments, useTranslation);
      const blob = new Blob([srtContent], { type: 'text/plain;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const baseName = selectedTask.fileName.replace(/\.[^.]+$/, '');
      a.download = useTranslation ? `${baseName}.translated.srt` : `${baseName}.srt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    },
    [selectedTask],
  );

  // 没有选中任务时显示空状态
  if (!selectedTask) {
    return (
      <Box
        sx={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          bgcolor: 'rgba(30, 34, 54, 0.4)',
          borderRadius: 2,
          border: '1px dashed rgba(124, 77, 255, 0.2)',
          p: 4,
        }}
      >
        <SubtitlesIcon sx={{ fontSize: 48, color: '#3D4266', mb: 2 }} />
        <Typography variant="body2" sx={{ color: '#5A6180', textAlign: 'center' }}>
          点击已完成的任务查看转录结果
        </Typography>
      </Box>
    );
  }

  const segments = selectedTask.segments;
  const translatedSegments = selectedTask.translatedSegments;
  const hasTranslation = selectedTask.translationStatus === 'done';
  const isTranslating = selectedTask.translationStatus === 'translating';
  const displaySegments = activeTab === 0 ? segments : translatedSegments;

  return (
    <Box
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        bgcolor: 'rgba(30, 34, 54, 0.6)',
        borderRadius: 2,
        border: '1px solid rgba(124, 77, 255, 0.15)',
        overflow: 'hidden',
      }}
    >
      {/* 头部：文件名 + 操作按钮 */}
      <Box
        sx={{
          px: 2,
          py: 1.5,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderBottom: '1px solid rgba(124, 77, 255, 0.1)',
        }}
      >
        <Typography
          variant="body2"
          sx={{
            color: '#E8EAF0',
            fontWeight: 600,
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            flex: 1,
            mr: 1,
          }}
        >
          {selectedTask.fileName}
        </Typography>

        <div className="flex items-center gap-1">
          {/* 翻译按钮 */}
          <Tooltip title={hasTranslation ? '重新翻译' : '翻译为中文'}>
            <span>
              <Button
                size="small"
                variant="outlined"
                disabled={
                  isTranslating ||
                  segments.length === 0
                }
                onClick={handleTranslate}
                startIcon={
                  isTranslating ? (
                    <CircularProgress size={14} sx={{ color: '#7C4DFF' }} />
                  ) : (
                    <TranslateIcon sx={{ fontSize: 16 }} />
                  )
                }
                sx={{
                  color: '#7C4DFF',
                  borderColor: 'rgba(124, 77, 255, 0.4)',
                  fontSize: '0.75rem',
                  textTransform: 'none',
                  '&:hover': {
                    borderColor: '#7C4DFF',
                    bgcolor: 'rgba(124, 77, 255, 0.08)',
                  },
                  '&.Mui-disabled': {
                    borderColor: 'rgba(124, 77, 255, 0.15)',
                    color: 'rgba(124, 77, 255, 0.3)',
                  },
                }}
              >
                {isTranslating ? '翻译中...' : '翻译'}
              </Button>
            </span>
          </Tooltip>

          {/* 关闭按钮 */}
          <Tooltip title="关闭">
            <IconButton
              size="small"
              onClick={() => selectTask(null)}
              sx={{ color: '#5A6180' }}
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </div>
      </Box>

      {/* Tab 栏：原文 / 译文 */}
      <Tabs
        value={activeTab}
        onChange={(_, v) => setActiveTab(v)}
        variant="fullWidth"
        sx={{
          minHeight: 36,
          borderBottom: '1px solid rgba(124, 77, 255, 0.1)',
          '& .MuiTab-root': {
            minHeight: 36,
            py: 0.5,
            fontSize: '0.8rem',
            fontWeight: 600,
            color: '#9EA3B8',
            '&.Mui-selected': { color: '#7C4DFF' },
          },
          '& .MuiTabs-indicator': {
            bgcolor: '#7C4DFF',
            height: 2,
          },
        }}
      >
        <Tab
          icon={<TextFieldsIcon sx={{ fontSize: 16 }} />}
          iconPosition="start"
          label={`原文 (${segments.length})`}
        />
        <Tab
          icon={<TranslateIcon sx={{ fontSize: 16 }} />}
          iconPosition="start"
          label={hasTranslation ? `译文 (${translatedSegments.length})` : '译文'}
          disabled={!hasTranslation}
        />
      </Tabs>

      {/* 内容区域：字幕列表 */}
      <Box
        sx={{
          flex: 1,
          overflow: 'auto',
          p: 1.5,
          '&::-webkit-scrollbar': { width: 6 },
          '&::-webkit-scrollbar-track': { bgcolor: 'transparent' },
          '&::-webkit-scrollbar-thumb': {
            bgcolor: 'rgba(124, 77, 255, 0.2)',
            borderRadius: 3,
          },
        }}
      >
        {selectedTask.status !== 'completed' ? (
          <Box
            sx={{
              height: '100%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Typography variant="body2" sx={{ color: '#5A6180' }}>
              任务进行中，请等待完成...
            </Typography>
          </Box>
        ) : displaySegments.length === 0 ? (
          <Box
            sx={{
              height: '100%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Typography variant="body2" sx={{ color: '#5A6180' }}>
              {activeTab === 1 ? '点击顶部"翻译"按钮生成译文' : '暂无转录内容'}
            </Typography>
          </Box>
        ) : (
          displaySegments.map((seg: SrtSegment) => (
            <Box
              key={seg.index}
              sx={{
                mb: 1.5,
                borderRadius: 1,
                bgcolor: 'rgba(42, 47, 74, 0.4)',
                borderLeft: '3px solid',
                borderLeftColor:
                  activeTab === 0
                    ? 'rgba(124, 77, 255, 0.5)'
                    : 'rgba(255, 152, 0, 0.5)',
                overflow: 'hidden',
                '&:hover': {
                  bgcolor: 'rgba(42, 47, 74, 0.7)',
                },
              }}
            >
              {/* 段落号 + 时间戳行 */}
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1,
                  px: 1.5,
                  pt: 0.8,
                  pb: 0.3,
                }}
              >
                <Typography
                  component="span"
                  sx={{
                    color: '#fff',
                    bgcolor: activeTab === 0 ? 'rgba(124,77,255,0.7)' : 'rgba(255,152,0,0.7)',
                    borderRadius: '4px',
                    px: 0.7,
                    py: 0.1,
                    fontSize: '0.68rem',
                    fontWeight: 700,
                    lineHeight: 1.6,
                    minWidth: 20,
                    textAlign: 'center',
                  }}
                >
                  {seg.index}
                </Typography>
                <Typography
                  variant="caption"
                  sx={{
                    color: activeTab === 0 ? '#7C4DFF' : '#FF9800',
                    fontWeight: 600,
                    fontFamily: 'monospace',
                    fontSize: '0.7rem',
                  }}
                >
                  {formatSrtTime(seg.startTime)} → {formatSrtTime(seg.endTime)}
                </Typography>
              </Box>
              {/* 正文 */}
              <Typography
                variant="body2"
                sx={{
                  color: '#E8EAF0',
                  px: 1.5,
                  pb: 0.8,
                  lineHeight: 1.6,
                  fontSize: '0.85rem',
                }}
              >
                {activeTab === 0 ? seg.text : seg.translatedText ?? seg.text}
              </Typography>
            </Box>
          ))
        )}
      </Box>

      {/* 底部：另存为 SRT */}
      <Box
        sx={{
          px: 2,
          py: 1.5,
          borderTop: '1px solid rgba(124, 77, 255, 0.1)',
          display: 'flex',
          gap: 1,
          justifyContent: 'flex-end',
        }}
      >
        <Button
          size="small"
          variant="outlined"
          disabled={segments.length === 0}
          onClick={() => handleSaveSrt(false)}
          startIcon={<SaveAltIcon sx={{ fontSize: 16 }} />}
          sx={{
            color: '#4CAF50',
            borderColor: 'rgba(76, 175, 80, 0.4)',
            fontSize: '0.75rem',
            textTransform: 'none',
            '&:hover': {
              borderColor: '#4CAF50',
              bgcolor: 'rgba(76, 175, 80, 0.08)',
            },
            '&.Mui-disabled': {
              borderColor: 'rgba(76, 175, 80, 0.15)',
              color: 'rgba(76, 175, 80, 0.3)',
            },
          }}
        >
          另存为 SRT
        </Button>
        {hasTranslation && (
          <Button
            size="small"
            variant="contained"
            onClick={() => handleSaveSrt(true)}
            startIcon={<SaveAltIcon sx={{ fontSize: 16 }} />}
            sx={{
              bgcolor: '#7C4DFF',
              fontSize: '0.75rem',
              textTransform: 'none',
              '&:hover': { bgcolor: '#6A3DE8' },
            }}
          >
            另存翻译 SRT
          </Button>
        )}
      </Box>
    </Box>
  );
};

export default ResultPanel;
