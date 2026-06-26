'use client';

import { SearchResult } from '../api/music';
import { Play, Clock } from 'lucide-react';

interface MusicResultsProps {
  results: SearchResult[];
  onTrackSelect: (track: SearchResult) => void;
}

export default function MusicResults({ results, onTrackSelect }: MusicResultsProps) {
  const formatDuration = (ms: number) => {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">搜索结果 ({results.length})</h2>
      <div className="grid gap-4">
        {results.map((track) => (
          <div
            key={track.id}
            className="bg-gray-800/50 backdrop-blur rounded-lg p-4 hover:bg-gray-800 transition-all cursor-pointer group"
            onClick={() => onTrackSelect(track)}
          >
            <div className="flex items-center gap-4">
              <img
                src={track.artwork_url}
                alt={track.name}
                className="w-16 h-16 rounded object-cover"
              />
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold truncate group-hover:text-green-400 transition-colors">
                  {track.name}
                </h3>
                <p className="text-sm text-gray-400 truncate">{track.artist}</p>
                <p className="text-xs text-gray-500 truncate">{track.album}</p>
              </div>
              <div className="flex items-center gap-4 text-sm text-gray-400">
                {track.duration && (
                  <div className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    {formatDuration(track.duration)}
                  </div>
                )}
                {track.preview_url && (
                  <button className="p-2 bg-green-500 rounded-full hover:bg-green-600 transition-colors">
                    <Play className="w-4 h-4" />
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
