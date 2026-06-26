'use client';

import { useState, useEffect } from 'react';
import { X, Music } from 'lucide-react';
import { musicApi, SearchResult } from '../api/music';

interface LyricsDisplayProps {
  track: SearchResult;
  onClose: () => void;
}

export default function LyricsDisplay({ track, onClose }: LyricsDisplayProps) {
  const [lyrics, setLyrics] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadLyrics();
  }, [track]);

  const loadLyrics = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await musicApi.getLyrics(track.artist, track.name);
      if (response.success) {
        setLyrics(response.lyrics);
      } else {
        setError('未找到歌词');
      }
    } catch (err) {
      setError('加载歌词失败');
      console.error('加载歌词失败:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-gray-900 rounded-lg max-w-2xl w-full max-h-[80vh] overflow-hidden">
        {/* 头部 */}
        <div className="flex items-center justify-between p-4 border-b border-gray-800">
          <div className="flex items-center gap-3">
            <Music className="w-5 h-5 text-green-500" />
            <div>
              <h3 className="font-semibold">{track.name}</h3>
              <p className="text-sm text-gray-400">{track.artist}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-800 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 歌词内容 */}
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {loading ? (
            <div className="flex justify-center py-8">
              <div className="spinner" />
            </div>
          ) : error ? (
            <div className="text-center py-8 text-gray-400">
              <Music className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>{error}</p>
            </div>
          ) : lyrics ? (
            <div className="whitespace-pre-wrap text-gray-300 leading-relaxed">
              {lyrics}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-400">
              <p>暂无歌词</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
