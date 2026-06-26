"""
Meeting Recorder - Audio recording and transcription
Author: ClawHub Skill
"""

import wave
import pyaudio
import os
from typing import Dict, Optional
import speech_recognition as sr


class MeetingRecorder:
    """Meeting audio recorder with transcription capabilities"""
    
    def __init__(self):
        self.recording = False
        self.audio_file = None
        self.frames = []
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        self.audio = None
        self.stream = None
    
    def start_recording(self, output_path: str) -> bool:
        """
        Start recording audio to file.
        
        Args:
            output_path: Path to save the audio file
        
        Returns:
            True if recording started successfully
        """
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            self.audio_file = output_path
            self.frames = []
            self.recording = True
            
            print(f"Recording started... Saving to {output_path}")
            return True
        except Exception as e:
            print(f"Error starting recording: {e}")
            return False
    
    def stop_recording(self) -> bool:
        """
        Stop recording and save audio file.
        
        Returns:
            True if recording stopped and saved successfully
        """
        if not self.recording:
            return False
        
        try:
            self.recording = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            
            # Save audio file
            with wave.open(self.audio_file, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
            
            print(f"Recording saved to {self.audio_file}")
            return True
        except Exception as e:
            print(f"Error stopping recording: {e}")
            return False
    
    def stop_and_transcribe(self) -> Dict:
        """
        Stop recording and transcribe audio to text.
        
        Returns:
            Dictionary with transcription results
        """
        if self.stop_recording():
            return self.transcribe_audio(self.audio_file)
        return {"error": "Failed to stop recording"}
    
    def transcribe_audio(self, audio_file: str) -> Dict:
        """
        Transcribe audio file to text.
        
        Args:
            audio_file: Path to audio file
        
        Returns:
            Dictionary with transcription text and metadata
        """
        recognizer = sr.Recognizer()
        
        try:
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
                
            text = recognizer.recognize_google(audio_data, language='zh-CN')
            
            return {
                "status": "success",
                "text": text,
                "audio_file": audio_file,
                "duration_seconds": len(audio_data.frame_data) / audio_data.sample_rate
            }
        except sr.UnknownValueError:
            return {
                "status": "error",
                "error": "Could not understand audio",
                "audio_file": audio_file
            }
        except sr.RequestError as e:
            return {
                "status": "error",
                "error": f"Recognition service error: {e}",
                "audio_file": audio_file
            }
    
    def transcribe_from_microphone(self, duration: int = 30) -> Dict:
        """
        Record and transcribe from microphone (short duration).
        
        Args:
            duration: Recording duration in seconds
        
        Returns:
            Dictionary with transcription results
        """
        recognizer = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                print(f"Recording from microphone for {duration} seconds...")
                audio_data = recognizer.record(source, duration=duration)
            
            text = recognizer.recognize_google(audio_data, language='zh-CN')
            
            return {
                "status": "success",
                "text": text,
                "duration_seconds": duration
            }
        except sr.UnknownValueError:
            return {
                "status": "error",
                "error": "Could not understand audio"
            }
        except sr.RequestError as e:
            return {
                "status": "error",
                "error": f"Recognition service error: {e}"
            }


if __name__ == "__main__":
    print("Meeting Recorder - Audio Recording and Transcription")
    print("=" * 50)
    
    # Example: Transcribe from microphone
    recorder = MeetingRecorder()
    # result = recorder.transcribe_from_microphone(duration=10)
    # print(f"Transcript: {result}")
