'use client';

import { useState, useEffect } from 'react';
import { Radio, Play, Volume2 } from 'lucide-react';
import { musicApi, RadioStation } from '../api/music';

interface RadioPlayerProps {
  stations: RadioStation[];
  onStationSelect: (station: RadioStation) => void;
  onStationsLoad: (stations: RadioStation[]) => void;
}

export default function RadioPlayer({ stations, onStationSelect, onStationsLoad }: RadioPlayerProps) {
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadTopStations();
  }, []);

  const loadTopStations = async () => {
    setLoading(true);
    try {
      const response = await musicApi.getTopRadio(20);
      if (response.success) {
        onStationsLoad(response.results);
      }
    } catch (error) {
      console.error('加载电台失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoading(true);
    try {
      const response = await musicApi.searchRadio({ name: searchQuery });
      if (response.success) {
        onStationsLoad(response.results);
      }
    } catch (error) {
      console.error('搜索电台失败:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-2 mb-4">
        <Radio className="w-6 h-6 text-green-500" />
        <h2 className="text-xl font-bold">网络电台</h2>
      </div>

      <form onSubmit={handleSearch} className="relative">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="搜索电台..."
          className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-green-500 transition-colors"
        />
      </form>

      {loading ? (
        <div className="flex justify-center py-8">
          <div className="spinner" />
        </div>
      ) : (
        <div className="grid gap-4">
          {stations.map((station) => (
            <div
              key={station.id}
              className="bg-gray-800/50 backdrop-blur rounded-lg p-4 hover:bg-gray-800 transition-all cursor-pointer group"
              onClick={() => onStationSelect(station)}
            >
              <div className="flex items-center gap-4">
                {station.favicon && (
                  <img
                    src={station.favicon}
                    alt={station.name}
                    className="w-12 h-12 rounded"
                    onError={(e) => {
                      e.currentTarget.style.display = 'none';
                    }}
                  />
                )}
                <div className="flex-1 min-w-0">
                  <h3 className="font-semibold truncate group-hover:text-green-400 transition-colors">
                    {station.name}
                  </h3>
                  <p className="text-sm text-gray-400">
                    {station.country} • {station.language}
                  </p>
                  <div className="flex gap-2 mt-1">
                    {station.tags.slice(0, 3).map((tag) => (
                      <span
                        key={tag}
                        className="text-xs px-2 py-1 bg-gray-700 rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-400">
                  {station.bitrate && (
                    <span>{station.bitrate}kbps</span>
                  )}
                  <button className="p-2 bg-green-500 rounded-full hover:bg-green-600 transition-colors">
                    <Play className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
