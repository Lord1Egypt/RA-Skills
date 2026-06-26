import React, { useCallback, useRef, useState } from 'react';
import {
  Box,
  Typography,
  Alert,
  Paper,
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import { useQueueStore } from '../store/queueStore';
import { getLanguageLabel, formatSrtTime } from '../utils/helpers';
import type { SrtSegment } from '../types';

/**
 * SRT 翻译页面 — 内容区，设置栏已移至 Header。
 * 布局：上传区 / 三列对照表格（段落号 | 原文 | 译文）。
 */
const SrtTranslatePage: React.FC = () => {
  const {
    srtSourceLanguage, srtTargetLanguage,
    srtSegments, srtTranslatedSegments, srtTranslateStatus, srtError,
    loadSrtFile,
  } = useQueueStore();

  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const isTranslating = srtTranslateStatus === 'translating';
  const isStopped = srtTranslateStatus === 'stopped';
  const isDone = srtTranslateStatus === 'done';
  const hasSegments = srtSegments.length > 0;

  // ─── 文件拖放处理 ─────────────────────────────────────
  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files?.[0]) {
      const file = e.dataTransfer.files[0];
      if (file.name.endsWith('.srt')) {
        loadSrtFile(file);
      }
    }
  }, [loadSrtFile]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) loadSrtFile(file);
  }, [loadSrtFile]);

  // 建立译文 index→segment 映射，方便按序号查找
  const translatedMap = new Map<number, SrtSegment>();
  for (const seg of srtTranslatedSegments) {
    translatedMap.set(seg.index, seg);
  }

  return (
    <Box
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        '&::-webkit-scrollbar': { width: 6 },
        '&::-webkit-scrollbar-track': { bgcolor: 'transparent' },
        '&::-webkit-scrollbar-thumb': { bgcolor: 'rgba(124,77,255,0.2)', borderRadius: 3 },
      }}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      {/* ── 错误提示 ───────────────────────────────── */}
      {srtError && (
        <Alert severity="error" sx={{ m: 2, borderRadius: 1.5, flexShrink: 0 }}>
          {srtError}
        </Alert>
      )}

      {/* ── 主要内容区 ─────────────────────────────── */}
      {!hasSegments ? (
        /* 上传区域 */
        <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', p: 8 }}>
          <Paper
            elevation={0}
            onClick={() => fileInputRef.current?.click()}
            sx={{
              width: 480, p: 6, textAlign: 'center', cursor: 'pointer',
              bgcolor: dragActive ? 'rgba(124,77,255,0.12)' : 'rgba(30,34,54,0.6)',
              border: `2px dashed ${dragActive ? '#7C4DFF' : 'rgba(124,77,255,0.25)'}`,
              borderRadius: 3, transition: 'all 0.2s',
              '&:hover': { borderColor: '#7C4DFF', bgcolor: 'rgba(124,77,255,0.08)' },
            }}
          >
            <UploadFileIcon sx={{ fontSize: 56, color: '#7C4DFF', mb: 2 }} />
            <Typography variant="h6" sx={{ color: '#E8EAF0', mb: 1 }}>
              拖拽 SRT 文件到此处
            </Typography>
            <Typography variant="body2" sx={{ color: '#9EA3B8' }}>
              或点击选择文件
            </Typography>
            <input
              ref={fileInputRef} type="file" accept=".srt,.SRT"
              style={{ display: 'none' }} onChange={handleFileSelect}
            />
          </Paper>
        </Box>
      ) : (
        /* ── 三列对照表格（段落号 | 原文 | 译文）────────────── */
        <Box
          sx={{
            flex: 1,
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            '&::-webkit-scrollbar': { width: 6 },
            '&::-webkit-scrollbar-track': { bgcolor: 'transparent' },
            '&::-webkit-scrollbar-thumb': { bgcolor: 'rgba(124,77,255,0.2)', borderRadius: 3 },
          }}
        >
          {/* 表头 */}
          <Box
            sx={{
              display: 'grid',
              gridTemplateColumns: '280px 1fr 1fr',
              gap: 0,
              position: 'sticky',
              top: 0,
              zIndex: 10,
              bgcolor: 'rgba(20,24,44,0.98)',
              borderBottom: '1px solid rgba(124,77,255,0.18)',
              px: 1.5,
              py: 1,
            }}
          >
            <Typography variant="caption" sx={{ color: '#5A6180', textAlign: 'center' }}>#</Typography>
            <Typography variant="caption" sx={{ color: '#9EA3B8', pl: 1 }}>
              原文（{getLanguageLabel(srtSourceLanguage)}）· {srtSegments.length} 段
            </Typography>
            <Typography variant="caption" sx={{ color: '#9EA3B8', pl: 1 }}>
              译文（{getLanguageLabel(srtTargetLanguage)}）
              {isTranslating
                ? ` · ${srtTranslatedSegments.length}/${srtSegments.length} 段`
                : (isDone || isStopped)
                  ? ` · ${srtTranslatedSegments.length} 段`
                  : ''}
            </Typography>
          </Box>

          {/* 逐行渲染 */}
          {srtSegments.map((seg) => {
            const translated = translatedMap.get(seg.index);
            const isPending = (isTranslating || isStopped) && !translated;
            return (
              <PairedRow
                key={seg.index}
                seg={seg}
                translatedText={translated?.translatedText}
                isPending={isPending}
                isStoppedRow={isStopped && !translated}
              />
            );
          })}
        </Box>
      )}
    </Box>
  );
};

// ─── PairedRow：一行显示段落号 + 原文 + 译文，三列对齐 ─────

interface PairedRowProps {
  seg: SrtSegment;
  translatedText?: string;
  isPending: boolean;
  isStoppedRow?: boolean;
}

const PairedRow: React.FC<PairedRowProps> = ({ seg, translatedText, isPending, isStoppedRow }) => {
  const timeLabel = `${formatSrtTime(seg.startTime)} --> ${formatSrtTime(seg.endTime)}`;

  return (
    <Box
      sx={{
        display: 'grid',
        gridTemplateColumns: '280px 1fr 1fr',
        gap: 0,
        borderBottom: '1px solid rgba(124,77,255,0.07)',
        bgcolor: seg.index % 2 === 0 ? 'transparent' : 'rgba(124,77,255,0.04)',
        '&:hover': { bgcolor: 'rgba(42,47,74,0.35)' },
        transition: 'background 0.15s',
      }}
    >
      {/* 段落号列 */}
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-end',
          justifyContent: 'flex-start',
          pt: 1.2,
          pb: 1,
          borderRight: '1px solid rgba(124,77,255,0.1)',
          bgcolor: 'rgba(20,24,44,0.4)',
          gap: 0.3,
        }}
      >
        <Typography
          variant="caption"
          sx={{
            color: '#7C4DFF', fontWeight: 700, fontSize: '0.72rem',
            lineHeight: 1, pr: 1,
          }}
        >
          {seg.index}
        </Typography>
        <Typography
          variant="caption"
          sx={{ color: '#3D4266', fontSize: '0.6rem', fontFamily: 'monospace', lineHeight: 1 }}
        >
          {timeLabel}
        </Typography>
      </Box>

      {/* 原文列 */}
      <Box
        sx={{
          px: 1.5, py: 1,
          borderRight: '1px solid rgba(124,77,255,0.1)',
          borderLeft: '3px solid rgba(124,77,255,0.5)',
        }}
      >
        <Typography variant="body2" sx={{ color: '#E8EAF0', lineHeight: 1.7, whiteSpace: 'pre-wrap', fontSize: '0.85rem' }}>
          {seg.text}
        </Typography>
      </Box>

      {/* 译文列 */}
      <Box
        sx={{
          px: 1.5, py: 1,
          borderLeft: '3px solid rgba(255,152,0,0.5)',
        }}
      >
        {isPending ? (
          <Box sx={{ display: 'flex', alignItems: 'center', height: '100%', minHeight: 28 }}>
            <Typography variant="body2" sx={{ color: '#3D4266', fontSize: '0.8rem' }}>—</Typography>
          </Box>
        ) : translatedText ? (
          <Typography variant="body2" sx={{ color: '#FFE0B2', lineHeight: 1.7, whiteSpace: 'pre-wrap', fontSize: '0.85rem' }}>
            {translatedText}
          </Typography>
        ) : isStoppedRow ? (
          <Box sx={{ display: 'flex', alignItems: 'center', height: '100%', minHeight: 28 }}>
            <Typography variant="body2" sx={{ color: '#5A6180', fontSize: '0.8rem', fontStyle: 'italic' }}>
              未翻译
            </Typography>
          </Box>
        ) : (
          <Box sx={{ display: 'flex', alignItems: 'center', height: '100%', minHeight: 28 }}>
            <Typography variant="body2" sx={{ color: '#5A6180', fontSize: '0.8rem', fontStyle: 'italic' }}>
              待翻译
            </Typography>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default SrtTranslatePage;
