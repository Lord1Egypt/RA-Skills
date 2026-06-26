import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export interface SearchResult {
  id: number;
  name: string;
  artist: string;
  album: string;
  duration: number;
  preview_url: string;
  artwork_url: string;
  genre: string;
  release_date: string;
  price: number;
  currency: string;
}

export interface LyricsResult {
  success: boolean;
  lyrics: string;
  artist: string;
  title: string;
}

export interface RadioStation {
  id: string;
  name: string;
  url: string;
  homepage: string;
  favicon: string;
  country: string;
  language: string;
  tags: string[];
  bitrate: number;
  codec: string;
  votes?: number;
}

export interface ArtistEvent {
  id: string;
  artist: string;
  venue: any;
  datetime: string;
  description: string;
  url: string;
  offers: any[];
}

export const musicApi = {
  // 搜索音乐
  async searchMusic(term: string, media: string = 'music', limit: number = 20) {
    const response = await api.get('/api/search', {
      params: { term, media, limit, country: 'CN' }
    });
    return response.data;
  },

  // 获取歌词
  async getLyrics(artist: string, title: string) {
    const response = await api.get('/api/lyrics', {
      params: { artist, title }
    });
    return response.data;
  },

  // 获取艺术家信息
  async getArtistInfo(artistId: string) {
    const response = await api.get(`/api/artist/${artistId}`);
    return response.data;
  },

  // 搜索电台
  async searchRadio(params: {
    name?: string;
    country?: string;
    tag?: string;
    limit?: number;
  }) {
    const response = await api.get('/api/radio/search', {
      params: { ...params, limit: params.limit || 20 }
    });
    return response.data;
  },

  // 获取热门电台
  async getTopRadio(limit: number = 20) {
    const response = await api.get('/api/radio/top', {
      params: { limit }
    });
    return response.data;
  },

  // 获取艺术家演唱会信息
  async getArtistEvents(artistName: string, date?: string) {
    const response = await api.get('/api/events', {
      params: { artist_name: artistName, date }
    });
    return response.data;
  },

  // 健康检查
  async healthCheck() {
    const response = await api.get('/api/health');
    return response.data;
  },
};

export default musicApi;
