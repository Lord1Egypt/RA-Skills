# File Category Mappings

Maps file extensions to organized folder names. Used by `organize.py` to generate move plans.

## Category Rules (extension → folder)

### Images
`.jpg` `.jpeg` `.png` `.gif` `.bmp` `.tiff` `.tif` `.webp` `.heic` `.heif` `.svg` `.ico` `.raw` `.cr2` `.nef` `.arw` → `Images`

### Videos
`.mp4` `.mov` `.avi` `.mkv` `.wmv` `.flv` `.m4v` `.webm` `.mpeg` `.mpg` `.3gp` `.ts` `.vob` → `Videos`

### Audio
`.mp3` `.wav` `.flac` `.aac` `.ogg` `.m4a` `.wma` `.opus` `.aiff` `.aif` → `Audio`

### Documents
`.pdf` `.doc` `.docx` `.odt` `.rtf` `.txt` `.md` `.pages` `.tex` `.epub` `.mobi` → `Documents`

### Spreadsheets
`.xls` `.xlsx` `.ods` `.csv` `.numbers` → `Spreadsheets`

### Presentations
`.ppt` `.pptx` `.odp` `.key` → `Presentations`

### Archives
`.zip` `.tar` `.gz` `.bz2` `.xz` `.7z` `.rar` `.tar.gz` `.tar.bz2` `.tar.xz` `.tgz` `.tbz2` `.dmg` `.iso` → `Archives`

### Code
`.py` `.js` `.ts` `.jsx` `.tsx` `.html` `.css` `.scss` `.sass` `.less` `.java` `.c` `.cpp` `.h` `.hpp` `.cs` `.go` `.rs` `.rb` `.php` `.swift` `.kt` `.r` `.m` `.sh` `.bash` `.zsh` `.fish` `.ps1` `.lua` `.sql` `.json` `.xml` `.yaml` `.yml` `.toml` `.ini` `.cfg` `.env` `.dockerfile` → `Code`

### Fonts
`.ttf` `.otf` `.woff` `.woff2` `.eot` → `Fonts`

### Disk Images & Installers
`.pkg` `.app` `.exe` `.msi` `.deb` `.rpm` → `Installers`

### Design
`.psd` `.ai` `.sketch` `.fig` `.xd` `.indd` `.afdesign` `.afphoto` `.afpub` → `Design`

### Data
`.db` `.sqlite` `.sqlite3` `.parquet` `.avro` `.npy` `.npz` `.pkl` `.joblib` → `Data`

## Fallback
Any extension not listed above → `Other`
