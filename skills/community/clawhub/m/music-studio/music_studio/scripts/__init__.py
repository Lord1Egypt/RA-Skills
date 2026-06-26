"""脚本命令实现"""

from music_studio.scripts import (
    init, lyrics, music, cover, library, clean, help as help_mod, reset, set_key, clear_key,
)

main = None

init_main = init.main
set_key_main = set_key.main
clear_key_main = clear_key.main
lyrics_main = lyrics.main
music_main = music.main
cover_main = cover.main
library_main = library.main
clean_main = clean.main
help_main = help_mod.main
reset_main = reset.main
