/**
 * MoodMusic — Conversation-Based Music Recommendations
 * @author @TheShadowRose
 * @license MIT
 */

const MOOD_KEYWORDS = {
  focus: ['work', 'focus', 'concentrate', 'study', 'coding', 'writing', 'productive'],
  energy: ['pump', 'energy', 'workout', 'exercise', 'hype', 'excited', 'motivated'],
  chill: ['relax', 'chill', 'calm', 'decompress', 'wind down', 'peaceful', 'easy'],
  sad: ['sad', 'down', 'depressed', 'lonely', 'miss', 'heartbreak', 'crying'],
  happy: ['happy', 'great', 'awesome', 'celebrate', 'joy', 'wonderful'],
  creative: ['creative', 'inspire', 'brainstorm', 'imagine', 'art', 'design']
};

const PLAYLISTS = {
  focus: [
    { artist: "Ludovico Einaudi", track: "Nuvole Bianche", genre: "classical" },
    { artist: "Tycho", track: "Awake", genre: "ambient" },
    { artist: "Bonobo", track: "Kerala", genre: "electronic" },
    { artist: "Emancipator", track: "First Snow", genre: "downtempo" },
    { artist: "Explosions in the Sky", track: "Your Hand in Mine", genre: "post-rock" }
  ],
  energy: [
    { artist: "Run The Jewels", track: "Close Your Eyes", genre: "hip-hop" },
    { artist: "The Prodigy", track: "Breathe", genre: "electronic" },
    { artist: "Rage Against The Machine", track: "Killing in the Name", genre: "rock" },
    { artist: "Daft Punk", track: "Around the World", genre: "electronic" },
    { artist: "Pendulum", track: "Watercolour", genre: "drum and bass" }
  ],
  chill: [
    { artist: "Norah Jones", track: "Don't Know Why", genre: "jazz" },
    { artist: "Khruangbin", track: "Maria También", genre: "psychedelic" },
    { artist: "Télépopmusik", track: "Breathe", genre: "trip-hop" },
    { artist: "The xx", track: "Intro", genre: "indie" },
    { artist: "Marconi Union", track: "Weightless", genre: "ambient" }
  ],
  sad: [
    { artist: "Bon Iver", track: "Skinny Love", genre: "indie folk" },
    { artist: "Radiohead", track: "Exit Music (For a Film)", genre: "alternative" },
    { artist: "Jeff Buckley", track: "Hallelujah", genre: "rock" },
    { artist: "Sleeping At Last", track: "Saturn", genre: "indie" },
    { artist: "Sigur Rós", track: "Svefn-g-englar", genre: "post-rock" }
  ],
  happy: [
    { artist: "Pharrell Williams", track: "Happy", genre: "pop" },
    { artist: "Earth Wind & Fire", track: "September", genre: "funk" },
    { artist: "Katrina & The Waves", track: "Walking on Sunshine", genre: "pop" },
    { artist: "OutKast", track: "Hey Ya!", genre: "hip-hop" },
    { artist: "Lizzo", track: "Good as Hell", genre: "pop" }
  ],
  creative: [
    { artist: "Brian Eno", track: "Music for Airports", genre: "ambient" },
    { artist: "Tame Impala", track: "Let It Happen", genre: "psychedelic" },
    { artist: "Flying Lotus", track: "Never Catch Me", genre: "experimental" },
    { artist: "Björk", track: "All is Full of Love", genre: "art pop" },
    { artist: "Glass Animals", track: "Gooey", genre: "indie" }
  ]
};

class MoodMusic {
  detectMood(text) {
    const lower = text.toLowerCase();
    const scores = {};
    for (const [mood, keywords] of Object.entries(MOOD_KEYWORDS)) {
      scores[mood] = keywords.filter(k => lower.includes(k)).length;
    }
    const best = Object.entries(scores).sort((a, b) => b[1] - a[1])[0];
    return best[1] > 0 ? best[0] : 'chill'; // default to chill
  }

  recommend(text, count = 5) {
    const mood = this.detectMood(text);
    const tracks = PLAYLISTS[mood] || PLAYLISTS.chill;
    const selected = tracks.slice(0, count);
    return {
      mood,
      tracks: selected,
      formatted: `🎵 ${mood.charAt(0).toUpperCase() + mood.slice(1)} mood detected\n\n` +
        selected.map(t => `🎵 ${t.track} — ${t.artist}`).join('\n')
    };
  }

  allMoods() { return Object.keys(PLAYLISTS); }
  getPlaylist(mood) { return PLAYLISTS[mood] || null; }
}

module.exports = { MoodMusic };
