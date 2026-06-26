import React, { useCallback, useEffect, useRef, useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Chip,
  Select,
  MenuItem,
  TextField,
  Button,
  LinearProgress,
  Menu,
  Fade,
  IconButton,
  Tooltip,
  type SelectChangeEvent,
} from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import TranslateIcon from '@mui/icons-material/Translate';
import StopIcon from '@mui/icons-material/Stop';
import DownloadIcon from '@mui/icons-material/Download';
import ArticleIcon from '@mui/icons-material/Article';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';
import { useQueueStore } from '../store/queueStore';
import { getShortModelName, LANGUAGES } from '../utils/helpers';
import type { PageName } from '../types';

/**
 * 顶部栏组件 — 显示应用标题、页面切换，翻译页时包含设置工具栏。
 */
const Header: React.FC = () => {
  // ── 转录页面状态 ───────────────────────────────────
  const settings = useQueueStore((s) => s.settings);
  const currentPage = useQueueStore((s) => s.currentPage);
  const defaultWhisperModelName = useQueueStore((s) => s.defaultWhisperModelName);
  const setCurrentPage = useQueueStore((s) => s.setCurrentPage);

  // ── SRT 翻译页面状态 ───────────────────────────────
  const srtSourceLanguage = useQueueStore((s) => s.srtSourceLanguage);
  const srtTargetLanguage = useQueueStore((s) => s.srtTargetLanguage);
  const srtTranslateModel = useQueueStore((s) => s.srtTranslateModel);
  const srtSegments = useQueueStore((s) => s.srtSegments);
  const srtTranslatedSegments = useQueueStore((s) => s.srtTranslatedSegments);
  const srtTranslateStatus = useQueueStore((s) => s.srtTranslateStatus);
  const srtTranslateStartTime = useQueueStore((s) => s.srtTranslateStartTime);
  const defaultTranslateModelName = useQueueStore((s) => s.defaultTranslateModelName);
  const setSrtSourceLanguage = useQueueStore((s) => s.setSrtSourceLanguage);
  const setSrtTargetLanguage = useQueueStore((s) => s.setSrtTargetLanguage);
  const setSrtTranslateModel = useQueueStore((s) => s.setSrtTranslateModel);
  const translateSrt = useQueueStore((s) => s.translateSrt);
  const stopTranslateSrt = useQueueStore((s) => s.stopTranslateSrt);
  const exportSrtOriginal = useQueueStore((s) => s.exportSrtOriginal);
  const exportSrtTranslated = useQueueStore((s) => s.exportSrtTranslated);
  const exportSrtBilingual = useQueueStore((s) => s.exportSrtBilingual);

  const isTranslating = srtTranslateStatus === 'translating';
  const isStopped = srtTranslateStatus === 'stopped';
  const isDone = srtTranslateStatus === 'done';
  const hasSegments = srtSegments.length > 0;
  const canExport = isDone || isStopped;

  const modelName = settings.modelPath
    ? getShortModelName(settings.modelPath)
    : defaultWhisperModelName || '默认';

  const handleTab = (page: PageName) => () => setCurrentPage(page);

  // ── SRT 翻译：模型目录选择 ─────────────────────────
  const modelDirInputRef = useRef<HTMLInputElement>(null);

  const handleModelDirPick = useCallback(async () => {
    if ('showDirectoryPicker' in window) {
      try {
        const dirHandle = await (window as any).showDirectoryPicker({ mode: 'read' });
        if (dirHandle) {
          setSrtTranslateModel(dirHandle.name);
          return;
        }
      } catch (e: any) {
        if (e?.name === 'AbortError') return;
      }
    }
    modelDirInputRef.current?.click();
  }, [setSrtTranslateModel]);

  const handleModelDirInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files.length > 0) {
        const relPath = files[0].webkitRelativePath;
        const dirName = relPath.split('/')[0];
        setSrtTranslateModel(dirName);
      }
      e.target.value = '';
    },
    [setSrtTranslateModel],
  );

  // ── SRT 翻译：导出菜单 ─────────────────────────────
  const [exportAnchor, setExportAnchor] = useState<null | HTMLElement>(null);
  const handleExportClick = (event: React.MouseEvent<HTMLElement>) => setExportAnchor(event.currentTarget);
  const handleExportClose = () => setExportAnchor(null);
  const handleExportOriginal = () => { handleExportClose(); exportSrtOriginal(); };
  const handleExportTranslated = () => { handleExportClose(); exportSrtTranslated(); };
  const handleExportBilingual = () => { handleExportClose(); exportSrtBilingual(); };

  // ── SRT 翻译：计时器 tick ──────────────────────────
  const [, setTick] = useState(0);
  useEffect(() => {
    if (srtTranslateStatus !== 'translating') { setTick(0); return; }
    const id = setInterval(() => setTick((t) => t + 1), 1000);
    return () => clearInterval(id);
  }, [srtTranslateStatus]);

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{
        background: 'linear-gradient(135deg, #1E2236 0%, #2A2F4A 100%)',
        borderBottom: '1px solid rgba(124, 77, 255, 0.15)',
      }}
    >
      {/* ── 主工具栏 ─────────────────────────────────── */}
      <Toolbar className="justify-between" sx={{ minHeight: '48px !important' }}>
        <div className="flex items-center gap-3">
          <MicIcon sx={{ color: '#7C4DFF', fontSize: 28 }} />
          <Box>
            <Typography
              variant="h6"
              sx={{
                fontWeight: 700,
                lineHeight: 1.2,
                background: 'linear-gradient(135deg, #7C4DFF, #B388FF)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
              }}
            >
              MLX Whisper 转录工具
            </Typography>
            <Typography
              variant="caption"
              sx={{ color: '#9EA3B8', display: 'block' }}
            >
              {currentPage === 'translate'
                ? defaultTranslateModelName
                  ? `翻译模型: ${defaultTranslateModelName}`
                  : 'SRT 翻译'
                : `${modelName} · 并发 ${settings.maxConcurrent}`}
            </Typography>
          </Box>
        </div>

        {/* 页面切换 Tabs */}
        <Box className="flex items-center gap-1">
          <Chip
            icon={<MicIcon sx={{ color: currentPage === 'transcribe' ? '#fff' : '#9EA3B8', fontSize: 18 }} />}
            label="转录队列"
            onClick={handleTab('transcribe')}
            sx={{
              bgcolor: currentPage === 'transcribe' ? '#7C4DFF' : 'rgba(42,47,74,0.5)',
              color: currentPage === 'transcribe' ? '#fff' : '#9EA3B8',
              fontWeight: currentPage === 'transcribe' ? 600 : 400,
              borderRadius: 1.5, cursor: 'pointer',
              '&:hover': { bgcolor: currentPage === 'transcribe' ? '#6B3FD4' : 'rgba(42,47,74,0.8)' },
              height: 34, '& .MuiChip-label': { px: 1.5 },
              '& .MuiChip-icon': { ml: 1 },
            }}
          />
          <Chip
            icon={<TranslateIcon sx={{ color: currentPage === 'translate' ? '#fff' : '#9EA3B8', fontSize: 18 }} />}
            label="SRT 翻译"
            onClick={handleTab('translate')}
            sx={{
              bgcolor: currentPage === 'translate' ? '#7C4DFF' : 'rgba(42,47,74,0.5)',
              color: currentPage === 'translate' ? '#fff' : '#9EA3B8',
              fontWeight: currentPage === 'translate' ? 600 : 400,
              borderRadius: 1.5, cursor: 'pointer',
              '&:hover': { bgcolor: currentPage === 'translate' ? '#6B3FD4' : 'rgba(42,47,74,0.8)' },
              height: 34, '& .MuiChip-label': { px: 1.5 },
              '& .MuiChip-icon': { ml: 1 },
            }}
          />
        </Box>
      </Toolbar>

      {/* ── SRT 翻译设置栏（仅在翻译页显示）─────────────── */}
      {currentPage === 'translate' && (
        <Box sx={{ px: 2, pb: 1.5, bgcolor: 'rgba(30,34,54,0.95)' }}>
          {/* 第一行：控件 */}
          <Box className="flex items-center gap-3 flex-wrap">
            {/* 源语言 */}
            <Box className="flex items-center gap-1.5">
              <Typography variant="caption" sx={{ color: '#9EA3B8', whiteSpace: 'nowrap' }}>
                源语言
              </Typography>
              <Select
                size="small"
                value={srtSourceLanguage}
                onChange={(e: SelectChangeEvent) => setSrtSourceLanguage(e.target.value)}
                disabled={isTranslating}
                sx={selectSx}
              >
                {LANGUAGES.map((l) => (
                  <MenuItem key={l.code} value={l.code}>{l.label}</MenuItem>
                ))}
              </Select>
            </Box>

            {/* 箭头 */}
            <Typography sx={{ color: '#7C4DFF', fontSize: 18 }}>→</Typography>

            {/* 目标语言 */}
            <Box className="flex items-center gap-1.5">
              <Typography variant="caption" sx={{ color: '#9EA3B8', whiteSpace: 'nowrap' }}>
                目标语言
              </Typography>
              <Select
                size="small"
                value={srtTargetLanguage}
                onChange={(e: SelectChangeEvent) => setSrtTargetLanguage(e.target.value)}
                disabled={isTranslating}
                sx={selectSx}
              >
                {LANGUAGES.filter((l) => l.code !== 'auto').map((l) => (
                  <MenuItem key={l.code} value={l.code}>{l.label}</MenuItem>
                ))}
              </Select>
            </Box>

            {/* 翻译模型 */}
            <TextField
              size="small"
              label="翻译模型"
              disabled={isTranslating}
              placeholder={defaultTranslateModelName ? `默认: ${defaultTranslateModelName}` : '留空使用默认'}
              value={srtTranslateModel}
              onChange={(e) => setSrtTranslateModel(e.target.value)}
              InputProps={{
                endAdornment: isTranslating ? undefined : (
                  <Tooltip title="浏览模型目录">
                    <IconButton size="small" sx={{ color: '#7C4DFF' }} onClick={handleModelDirPick}>
                      <FolderOpenIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                ),
              }}
              sx={textFieldSx}
            />

            {/* 翻译 / 停止 / 继续按钮 */}
            {isTranslating ? (
              <Button
                variant="contained"
                onClick={stopTranslateSrt}
                startIcon={<StopIcon />}
                sx={{
                  bgcolor: '#D32F2F', '&:hover': { bgcolor: '#B71C1C' },
                  borderRadius: 1.5, textTransform: 'none', fontWeight: 600,
                }}
              >
                停止翻译
              </Button>
            ) : isStopped ? (
              <Button
                variant="contained"
                disabled={!hasSegments}
                onClick={translateSrt}
                startIcon={<TranslateIcon />}
                sx={{
                  bgcolor: '#7C4DFF', '&:hover': { bgcolor: '#6B3FD4' },
                  '&.Mui-disabled': { bgcolor: 'rgba(124,77,255,0.3)', color: 'rgba(255,255,255,0.5)' },
                  borderRadius: 1.5, textTransform: 'none', fontWeight: 600,
                }}
              >
                继续翻译
              </Button>
            ) : (
              <Button
                variant="contained"
                disabled={!hasSegments}
                onClick={translateSrt}
                startIcon={<TranslateIcon />}
                sx={{
                  bgcolor: '#7C4DFF', '&:hover': { bgcolor: '#6B3FD4' },
                  '&.Mui-disabled': { bgcolor: 'rgba(124,77,255,0.3)', color: 'rgba(255,255,255,0.5)' },
                  borderRadius: 1.5, textTransform: 'none', fontWeight: 600,
                }}
              >
                翻译
              </Button>
            )}

            {/* 导出按钮 */}
            <Button
              variant="outlined"
              disabled={!hasSegments}
              onClick={handleExportClick}
              startIcon={<DownloadIcon />}
              sx={{
                borderColor: 'rgba(124,77,255,0.4)', color: '#B388FF',
                borderRadius: 1.5, textTransform: 'none',
                '&:hover': { borderColor: '#7C4DFF', bgcolor: 'rgba(124,77,255,0.1)' },
              }}
            >
              导出
            </Button>
            <Menu
              anchorEl={exportAnchor} open={Boolean(exportAnchor)}
              onClose={handleExportClose} TransitionComponent={Fade}
              PaperProps={{ sx: { bgcolor: '#1E2236', border: '1px solid rgba(124,77,255,0.2)' } }}
            >
              <MenuItem onClick={handleExportOriginal} sx={{ color: '#E8EAF0' }}>
                <ArticleIcon fontSize="small" sx={{ mr: 1, color: '#9EA3B8' }} />
                导出原文 SRT
              </MenuItem>
              <MenuItem onClick={handleExportTranslated} disabled={!canExport} sx={{ color: '#E8EAF0' }}>
                <ArticleIcon fontSize="small" sx={{ mr: 1, color: '#9EA3B8' }} />
                导出译文 SRT
              </MenuItem>
              <MenuItem onClick={handleExportBilingual} disabled={!canExport} sx={{ color: '#E8EAF0' }}>
                <ArticleIcon fontSize="small" sx={{ mr: 1, color: '#9EA3B8' }} />
                导出双语 SRT
              </MenuItem>
            </Menu>
          </Box>

          {/* 第二行：翻译进度 */}
          {(isTranslating || isStopped) && (
            <Box sx={{ mt: 1.5 }}>
              <LinearProgress
                variant="determinate"
                value={srtSegments.length > 0 ? (srtTranslatedSegments.length / srtSegments.length) * 100 : 0}
                sx={{
                  height: 6, borderRadius: 3,
                  '& .MuiLinearProgress-bar': { bgcolor: '#7C4DFF', borderRadius: 3, transition: 'transform 0.4s ease' },
                  bgcolor: 'rgba(124,77,255,0.12)',
                }}
              />
              <Box sx={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', mt: 0.6 }}>
                <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 1.5 }}>
                  <Typography variant="body2" sx={{ color: '#E8EAF0', fontWeight: 600, fontSize: '0.85rem' }}>
                    {isStopped ? '已停止' : '翻译进度'}
                  </Typography>
                  <Typography variant="body2" sx={{ color: '#B388FF', fontWeight: 700, fontSize: '0.9rem' }}>
                    {srtSegments.length > 0 ? Math.round((srtTranslatedSegments.length / srtSegments.length) * 100) : 0}%
                  </Typography>
                  <Typography variant="caption" sx={{ color: '#9EA3B8' }}>
                    {srtTranslatedSegments.length} / {srtSegments.length} 段
                  </Typography>
                </Box>

                {/* 时间信息（仅翻译中） */}
                {isTranslating && srtTranslateStartTime > 0 && (() => {
                  const elapsed = Math.max(0, (Date.now() - srtTranslateStartTime) / 1000);
                  const completed = srtTranslatedSegments.length;
                  const total = srtSegments.length;
                  const remaining = completed > 0
                    ? Math.max(0, (elapsed / completed) * (total - completed))
                    : 0;

                  const fmtTime = (s: number) => {
                    const m = Math.floor(s / 60);
                    const sec = Math.floor(s % 60);
                    return `${m}:${String(sec).padStart(2, '0')}`;
                  };

                  return (
                    <Box sx={{ display: 'flex', gap: 2 }}>
                      <Typography variant="caption" sx={{ color: '#5A6180' }}>
                        已用 <span style={{ color: '#9EA3B8', fontWeight: 600 }}>{fmtTime(elapsed)}</span>
                      </Typography>
                      <Typography variant="caption" sx={{ color: '#5A6180' }}>
                        预计剩余 <span style={{ color: '#FFB74D', fontWeight: 600 }}>{fmtTime(remaining)}</span>
                      </Typography>
                    </Box>
                  );
                })()}
              </Box>
            </Box>
          )}
        </Box>
      )}

      {/* 隐藏的目录选择 input（回退方案） */}
      <input
        ref={modelDirInputRef}
        type="file"
        style={{ display: 'none' }}
        {...{ webkitdirectory: '', directory: '' }}
        onChange={handleModelDirInputChange}
      />
    </AppBar>
  );
};

// ─── 样式 ─────────────────────────────────────────────

const selectSx = {
  color: '#E8EAF0', bgcolor: 'rgba(42,47,74,0.6)', borderRadius: 1.5,
  minWidth: 110, height: 34,
  '& .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(124,77,255,0.2)' },
  '&:hover .MuiOutlinedInput-notchedOutline': { borderColor: 'rgba(124,77,255,0.4)' },
  '&.Mui-focused .MuiOutlinedInput-notchedOutline': { borderColor: '#7C4DFF' },
  '& .MuiSvgIcon-root': { color: '#9EA3B8' },
};

const textFieldSx = {
  '& .MuiOutlinedInput-root': {
    color: '#E8EAF0', bgcolor: 'rgba(42,47,74,0.6)', borderRadius: 1.5,
    height: 34,
    '& fieldset': { borderColor: 'rgba(124,77,255,0.2)' },
    '&:hover fieldset': { borderColor: 'rgba(124,77,255,0.4)' },
    '&.Mui-focused fieldset': { borderColor: '#7C4DFF' },
  },
  '& .MuiInputLabel-root': { color: '#9EA3B8', fontSize: '0.85rem', '&.Mui-focused': { color: '#7C4DFF' } },
  width: 180,
};

export default Header;
