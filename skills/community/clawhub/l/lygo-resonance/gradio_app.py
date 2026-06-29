#!/usr/bin/env python3
"""
LYGO RESONANCE - Gradio GUI
Web interface for the Resonance Engine and Profile Generator.
Full source from https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html
"""

import gradio as gr
import os
import json
from pathlib import Path
from resonance_engine import ResonanceEngine, PRESETS
from lygo_profile import LYGOProfileGenerator

def process_image(image_path, engine_type, style, seed, duration, noise_filter, 
                  export_stems, export_midi, export_brief, use_batch, batch_folder):
    
    # 1. Validation guardrails
    if not image_path and not use_batch:
        return "⚠️ Error: Please upload an image or enable batch processing mode.", None, None

    # 2. Setup output collections for file download components
    downloadable_files = []
    playback_audio = None

    try:
        # --- BATCH PROCESSING MODE ---
        if use_batch and batch_folder:
            folder = Path(batch_folder)
            if not folder.is_dir():
                return f"❌ Error: Batch folder path '{batch_folder}' does not exist or is invalid.", None, None
            
            images = sorted(folder.glob("*.jpg")) + sorted(folder.glob("*.png")) + sorted(folder.glob("*.jpeg"))
            if not images:
                return f"ℹ️ Notice: No compatible images (.jpg, .jpeg, .png) found in '{batch_folder}'.", None, None
            
            results = []
            for img in images:
                try:
                    if engine_type == "Resonance Engine (Audio)":
                        out_path = f"resonance_{img.stem}.wav"
                        config = {
                            "duration": duration,
                            "random_seed": int(seed) if seed != 0 else None,
                            "verbose": False,
                            "export_stems": export_stems,
                            "export_midi": export_midi,
                        }
                        if noise_filter > 0:
                            config["noise_lowpass_hz"] = noise_filter
                        
                        preset = PRESETS.get(style, {})
                        config.update(preset)
                        
                        engine = ResonanceEngine(config)
                        engine.process(str(img), out_path)
                        results.append(f"✓ {img.name} → {out_path}")
                        downloadable_files.append(out_path)
                        
                    else:
                        out_json = f"lygo_profile_{img.stem}.json"
                        generator = LYGOProfileGenerator(verbose=False)
                        generator.generate(str(img), out_json, create_brief=export_brief)
                        results.append(f"✓ {img.name} → {out_json}")
                        downloadable_files.append(out_json)
                        if export_brief:
                            downloadable_files.append(out_json.replace(".json", ".brief.txt"))
                            
                except Exception as batch_err:
                    results.append(f"✗ {img.name} → Error: {str(batch_err)}")
                    
            return "📦 Batch Processing Logs:\n" + "\n".join(results), None, downloadable_files

        # --- SINGLE IMAGE MODE ---
        img_p = Path(image_path)
        
        if engine_type == "Resonance Engine (Audio)":
            out_path = f"resonance_{img_p.stem}.wav"
            config = {
                "duration": duration,
                "random_seed": int(seed) if seed != 0 else None,
                "verbose": False,
                "export_stems": export_stems,
                "export_midi": export_midi,
            }
            if noise_filter > 0:
                config["noise_lowpass_hz"] = noise_filter
                
            preset = PRESETS.get(style, {})
            config.update(preset)
            
            engine = ResonanceEngine(config)
            engine.process(image_path, out_path)
            
            downloadable_files.append(out_path)
            playback_audio = out_path # Feed directly to audio player
            
            # Catch accompanying files if checked
            if export_midi:
                mid_file = out_path.replace(".wav", ".mid")
                if os.path.exists(mid_file):
                    downloadable_files.append(mid_file)
            if export_stems:
                for stem in ["noise", "drone", "melody", "glitch"]:
                    stem_file = out_path.replace(".wav", f"_{stem}.wav")
                    if os.path.exists(stem_file):
                        downloadable_files.append(stem_file)
                        
            log_msg = f"✅ Resonance Engine Matrix Complete.\nGenerated Stereo Mixdown: {out_path}"
            return log_msg, playback_audio, downloadable_files
            
        else:
            # LYGO Profile Mode
            out_json = f"lygo_profile_{img_p.stem}.json"
            generator = LYGOProfileGenerator(verbose=False)
            generator.generate(image_path, out_json, create_brief=export_brief)
            
            downloadable_files.append(out_json)
            
            # Read profile payload back to show the user the prompt data directly
            with open(out_json, "r", encoding="utf-8") as f:
                payload = json.load(f)
            
            ai_prompt = payload.get("LYGO_PROFILE", {}).get("ai_music_prompt", "Profile created.")
            log_msg = f"✅ LYGO DNA Profile Compiled Successfully!\nSaved Destination: {out_json}\n\n📋 AI Music Prompt Copy-Ready:\n\"{ai_prompt}\""
            
            if export_brief:
                brief_file = out_json.replace(".json", ".brief.txt")
                if os.path.exists(brief_file):
                    downloadable_files.append(brief_file)
                    
            return log_msg, None, downloadable_files

    except Exception as global_err:
        return f"❌ System Error executing core logic: {str(global_err)}", None, None

# --- DESIGN & LAYOUT THE INTERFACE ---
with gr.Blocks(theme=gr.themes.Box()) as demo:
    gr.Markdown("# 🌌 LYGO RESONANCE")
    gr.Markdown("### Core SDK Deployment — Visual-to-Audio Translation & Structural DNA Engine")
    
    with gr.Row():
        with gr.Column(scale=1):
            # Input block
            img_input = gr.Image(type="filepath", label="📸 Upload Source Image (Single File)")
            engine_choice = gr.Radio(
                ["Resonance Engine (Audio)", "LYGO Profile Generator"], 
                value="Resonance Engine (Audio)", 
                label="⚙️ Active Core Engine"
            )
            
            with gr.Accordion("🎨 Audio Synth Parameters (Resonance Engine)", open=True):
                preset_style = gr.Dropdown(
                    ["cinematic", "ambient", "glitch", "ethereal", "raw"], 
                    value="cinematic", 
                    label="Artistic Preset Blueprint"
                )
                duration_slider = gr.Slider(5, 60, value=15, step=1, label="Track Duration Length (Seconds)")
                seed_num = gr.Number(value=0, label="Mathematical Seed Lock (0 = Generative Continuous)")
                filter_hz = gr.Number(value=0, label="Noise Layer Lowpass Filter (Hz, 0 = Off)")
                stem_check = gr.Checkbox(label="Export Separated Audio Stems (.wav split)")
                midi_check = gr.Checkbox(label="Export Extracted Melodic MIDI Sequence")
                
            with gr.Accordion("📝 Analytical Parameters (Profile Engine)", open=False):
                brief_check = gr.Checkbox(value=True, label="Generate Human-Readable Brief (.brief.txt)")
                
            with gr.Accordion("📂 Automated Batch Processing Cluster", open=False):
                batch_check = gr.Checkbox(label="Activate Mass Batch Folder Mode")
                batch_dir = gr.Textbox(
                    label="Local Server Input Folder Directory", 
                    placeholder="e.g., ./input_folder"
                )
                
            submit_btn = gr.Button("🔮 Execute Spectral Scan", variant="primary")

        with gr.Column(scale=1):
            # Output block
            text_output = gr.Textbox(label="🖥️ Core Diagnostics Log & Text Prompts", lines=10, interactive=False)
            audio_player = gr.Audio(label="🎧 Real-Time Stereo Mix Down Preview", interactive=False)
            file_download = gr.Files(label="📦 Download Output Manifest (WAV, JSON, MID, TXT)", interactive=False)

    # Attach event processing hook
    submit_btn.click(
        fn=process_image,
        inputs=[
            img_input, engine_choice, preset_style, seed_num, duration_slider, filter_hz,
            stem_check, midi_check, brief_check, batch_check, batch_dir
        ],
        outputs=[text_output, audio_player, file_download]
    )

if __name__ == "__main__":
    demo.launch()