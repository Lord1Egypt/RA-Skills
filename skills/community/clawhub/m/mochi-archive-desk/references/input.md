# JSON actions

Actions inspect(file), extract(file,directory), create(files:[workspace-relative files],output). Compressed input<=100MiB, expanded<=100MiB and <=5000 entries. No links, encrypted entries, traversal, file/directory collisions or device paths. Outputs and directory must be new. ZIP creation accepts ordinary files explicitly, not implicit directory recursion; use an inventory of the desired folder to choose files. Output includes archive and per-file SHA256. Example file in samples/example.txt.
