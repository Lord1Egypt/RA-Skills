#!/usr/bin/env python3
"""
LYGO LLM Integration
Expands LYGO creative briefs into full song lyrics using local LLMs (Ollama, llama.cpp, etc.)
Full source from https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html
"""

import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any

class LYGOLLMExpander:
    def __init__(self, llm_url: str = "http://localhost:11434/api/generate", 
                 model: str = "llama3.2", verbose: bool = True):
        self.llm_url = llm_url
        self.model = model
        self.verbose = verbose
    
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def expand_brief_to_lyrics(self, brief_path: Path, output_path: Optional[Path] = None) -> str:
        """Read a LYGO creative brief and generate full song lyrics using a local LLM."""
        with open(brief_path, 'r', encoding='utf-8') as f:
            brief = f.read()
        
        self._log(f"Reading brief: {brief_path}")
        
        prompt = f"""You are a professional songwriter. Based on the following creative brief, write a complete song with a title, verses, a chorus, a bridge, and an outro. Use vivid imagery and emotional depth.

Creative Brief:
{brief}

Now write the song. Include a title at the top."""
        
        self._log(f"Contacting LLM at {self.llm_url} with model {self.model}...")
        
        try:
            response = requests.post(
                self.llm_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.8,
                },
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            lyrics = result.get("response", "No response from LLM.")
            
            if output_path is None:
                output_path = brief_path.with_suffix(".lyrics.txt")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(lyrics)
            
            self._log(f"✓ Lyrics saved: {output_path}")
            return lyrics
        
        except requests.exceptions.ConnectionError:
            error_msg = "Error: Could not connect to LLM. Make sure Ollama or llama.cpp is running."
            self._log(error_msg)
            return error_msg
        except Exception as e:
            self._log(f"Error: {str(e)}")
            return str(e)
    
    def batch_process_folder(self, folder_path: Path, output_folder: Optional[Path] = None):
        """Process all .brief.txt files in a folder."""
        briefs = list(folder_path.glob("*.brief.txt"))
        if not briefs:
            self._log("No .brief.txt files found in folder.")
            return
        
        if output_folder is None:
            output_folder = folder_path
        
        output_folder.mkdir(parents=True, exist_ok=True)
        
        for brief in briefs:
            out_path = output_folder / brief.with_suffix(".lyrics.txt").name
            self._log(f"Processing: {brief.name}")
            self.expand_brief_to_lyrics(brief, out_path)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="LYGO LLM Expander — Turn creative briefs into full lyrics using local LLMs"
    )
    parser.add_argument("input", help="Path to .brief.txt file or folder (with --batch)")
    parser.add_argument("-o", "--output", default=None, help="Output path or folder")
    parser.add_argument("--llm-url", default="http://localhost:11434/api/generate",
                        help="Ollama/llama.cpp API URL")
    parser.add_argument("--model", default="llama3.2", help="LLM model name")
    parser.add_argument("--batch", action="store_true", help="Process all .brief.txt files in folder")
    args = parser.parse_args()
    
    expander = LYGOLLMExpander(llm_url=args.llm_url, model=args.model)
    
    if args.batch:
        folder = Path(args.input)
        if not folder.is_dir():
            print("Error: --batch requires a folder path")
            return
        expander.batch_process_folder(folder, Path(args.output) if args.output else None)
    else:
        brief_path = Path(args.input)
        if not brief_path.exists():
            print("Error: File not found")
            return
        output_path = Path(args.output) if args.output else None
        expander.expand_brief_to_lyrics(brief_path, output_path)


if __name__ == "__main__":
    main()