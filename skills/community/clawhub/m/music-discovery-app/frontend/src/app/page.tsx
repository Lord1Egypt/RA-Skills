'use client';

import { useState } from 'react';
import SearchBar from '../components/SearchBar';
import MusicResults from '../components/MusicResults';
import RadioPlayer from '../components/RadioPlayer';
import LyricsDisplay from '../components/LyricsDisplay';
import { SearchResult, RadioStation } from '../api/music';

export default function Home() {
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [selectedTrack, setSelectedTrack] = useState<SearchResult | null>(null);
  const [radioStations, setRadioStations] = useState<RadioStation[]>([]);
  const [selectedStation, setSelectedStation] = useState<RadioStation | null>(null);
  const [showLyrics, setShowLyrics] = useState(false);
  const [activeTab, setActiveTab] = useState<'search' | 'radio'>('search');

  const handleSearch = (results: SearchResult[]) => {
    setSearchResults(results);
  };

  const handleTrackSelect = (track: SearchResult) => {
    setSelectedTrack(track);
    setShowLyrics(true);
  };

  const handleRadioSelect = (station: RadioStation) => {
    setSelectedStation(station);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black">
      {/* 头部 */}
      <header className="bg-black/50 backdrop-blur-lg border-b border-gray-800 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              <span className="text-3xl">🎵</span>
              音乐发现
            </h1>
            <div className="flex gap-2">
              <button
                onClick={() => setActiveTab('search')}
                className={`px-4 py-2 rounded-lg transition-all ${
                  activeTab === 'search'
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                }`}
              >
                搜索
              </button>
              <button
                onClick={() => setActiveTab('radio')}
                className={`px-4 py-2 rounded-lg transition-all ${
                  activeTab === 'radio'
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                }`}
              >
                电台
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* 主内容 */}
      <main className="container mx-auto px-4 py-8">
        {activeTab === 'search' ? (
          <div className="space-y-6">
            <SearchBar onSearch={handleSearch} />
            {searchResults.length > 0 && (
              <MusicResults
                results={searchResults}
                onTrackSelect={handleTrackSelect}
              />
            )}
          </div>
        ) : (
          <RadioPlayer
            stations={radioStations}
            onStationSelect={handleRadioSelect}
            onStationsLoad={setRadioStations}
          />
        )}
      </main>

      {/* 歌词显示 */}
      {showLyrics && selectedTrack && (
        <LyricsDisplay
          track={selectedTrack}
          onClose={() => setShowLyrics(false)}
        />
      )}

      {/* 底部播放器 */}
      {selectedTrack && (
        <div className="fixed bottom-0 left-0 right-0 bg-black/90 backdrop-blur-lg border-t border-gray-800 p-4">
          <div className="container mx-auto flex items-center gap-4">
            <img
              src={selectedTrack.artwork_url}
              alt={selectedTrack.name}
              className="w-12 h-12 rounded"
            />
            <div className="flex-1">
              <h3 className="font-semibold">{selectedTrack.name}</h3>
              <p className="text-sm text-gray-400">{selectedTrack.artist}</p>
            </div>
            {selectedTrack.preview_url && (
              <audio
                controls
                src={selectedTrack.preview_url}
                className="h-10"
              />
            )}
          </div>
        </div>
      )}
    </div>
  );
}
