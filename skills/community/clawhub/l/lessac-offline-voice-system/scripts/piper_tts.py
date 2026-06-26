#!/usr/bin/env python3
from tts_edge_wrapper import text_to_speech
import sys
if __name__ == '__main__':
    text = sys.argv[1] if len(sys.argv)>1 else ''
    out = sys.argv[2] if len(sys.argv)>2 else None
    voice = sys.argv[3] if len(sys.argv)>3 else None
    print(text_to_speech(text, out, voice=voice or 'en-IE-ConnorNeural'))
