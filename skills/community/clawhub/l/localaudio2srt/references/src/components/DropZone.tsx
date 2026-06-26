import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Box, Typography } from '@mui/material';
import AudioFileIcon from '@mui/icons-material/AudioFile';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { useQueueStore } from '../store/queueStore';
import { AUDIO_ACCEPT } from '../utils/helpers';

/**
 * 拖拽上传区域组件 — 仅接受音频文件。
 */
const DropZone: React.FC = () => {
  const addTask = useQueueStore((s) => s.addTask);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      for (const file of acceptedFiles) {
        addTask(file);
      }
    },
    [addTask],
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: AUDIO_ACCEPT,
    multiple: true,
  });

  return (
    <Box
      {...getRootProps()}
      sx={{
        border: '2px dashed',
        borderColor: isDragActive ? '#7C4DFF' : 'rgba(124, 77, 255, 0.3)',
        borderRadius: 3,
        p: 4,
        textAlign: 'center',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
        background: isDragActive
          ? 'rgba(124, 77, 255, 0.08)'
          : 'rgba(30, 34, 54, 0.5)',
        '&:hover': {
          borderColor: '#7C4DFF',
          background: 'rgba(124, 77, 255, 0.05)',
        },
      }}
    >
      <input {...getInputProps()} />

      {isDragActive ? (
        <div className="flex flex-col items-center gap-2 animate-fade-in">
          <CloudUploadIcon sx={{ fontSize: 48, color: '#7C4DFF' }} />
          <Typography variant="h6" sx={{ color: '#7C4DFF', fontWeight: 600 }}>
            释放音频文件以添加到转录队列
          </Typography>
        </div>
      ) : (
        <div className="flex flex-col items-center gap-2">
          <AudioFileIcon sx={{ fontSize: 48, color: '#5A6180' }} />
          <Typography variant="h6" sx={{ color: '#9EA3B8', fontWeight: 600 }}>
            拖拽音频文件到这里，或点击选择
          </Typography>
          <Typography variant="body2" sx={{ color: '#5A6180' }}>
            支持 M4A、WAV、MP3、FLAC、OGG、AAC、WMA 格式
          </Typography>
        </div>
      )}
    </Box>
  );
};

export default DropZone;
