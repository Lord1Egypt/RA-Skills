import modal
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, "/root/src")
import config
import images


def _bootstrap_cache():
    models_dir = Path(config.MOUNT_MODELS)
    cache_dir = Path.home() / ".cache"
    if not cache_dir.is_symlink():
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        cache_dir.parent.mkdir(parents=True, exist_ok=True)
        cache_dir.symlink_to(models_dir, target_is_directory=True)
    models_dir.mkdir(parents=True, exist_ok=True)


def _move_into(src: Path, dst_dir: Path):
    if src.name == "images" and (dst_dir / "images").exists():
        return
    dst = dst_dir / src.name
    if dst.exists():
        return
    shutil.move(str(src), str(dst))


def _flatten_and_save(work_dir: Path, stem: str):
    nested_pdf_dir = work_dir / stem
    if nested_pdf_dir.exists():
        for f in nested_pdf_dir.iterdir():
            if f.is_dir():
                if f.name == "auto":
                    for f2 in f.iterdir():
                        _move_into(f2, work_dir)
                else:
                    _move_into(f, work_dir)
            else:
                _move_into(f, work_dir)
        shutil.rmtree(nested_pdf_dir)
    nested_auto_dir = work_dir / "auto"
    if nested_auto_dir.exists():
        for f in nested_auto_dir.iterdir():
            _move_into(f, work_dir)
        shutil.rmtree(nested_auto_dir)


@images.app.function(
    image=images.image_ocr2markdown,
    gpu=config.GPU_TYPE,
    volumes={
        config.MOUNT_DATA: images.volume_data,
        config.MOUNT_MODELS: images.volume_models,
    },
    timeout=config.TIMEOUT_OCR2MD,
    retries=0,
)
def ocr2markdown(slug: str) -> list[dict]:
    _bootstrap_cache()
    upload_dir = Path(config.MOUNT_DATA) / slug / config.DIR_UPLOAD
    output_base = Path(config.MOUNT_DATA) / slug / config.DIR_OUTPUT
    pdf_files = sorted(upload_dir.glob("*.pdf"))
    if not pdf_files:
        return []
    results = []
    for pdf_path in pdf_files:
        stem = pdf_path.stem
        work_dir = output_base / f"{stem}_ocr"
        md_file = work_dir / f"{stem}.md"
        if md_file.exists():
            print(f"  [skip] {stem}.pdf")
            continue
        work_dir.mkdir(parents=True, exist_ok=True)
        print(f"  [proc] {stem}.pdf")
        t1 = time.monotonic()
        res = subprocess.run(
            ["mineru", "-p", str(pdf_path), "-o", str(work_dir), "-b", "pipeline"],
            capture_output=True,
            text=True,
        )
        elapsed = time.monotonic() - t1
        if res.returncode != 0:
            print(f"    ERROR: {res.stderr[-500:]}")
            continue
        _flatten_and_save(work_dir, stem)
        if md_file.exists():
            print(f"    done in {elapsed:.1f}s")
            results.append({"pdf": pdf_path.name, "elapsed": elapsed})
    return results


@images.app.local_entrypoint()
def main(slug: str) -> None:
    print(f"[ocr2markdown] processing: {slug}")
    results = ocr2markdown.remote(slug)
    print(f"\n[ocr2markdown] done. {len(results)} PDF(s) processed")
